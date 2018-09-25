#!/usr/bin/env python
import os
import sys
import logging
import redis
import json
import atexit
import time

CROWDAI_DEBUG_MODE = os.getenv("CROWDAI_DEBUG_MODE", False)
if CROWDAI_DEBUG_MODE:
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
else:
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__, )

class CrowdAIEvents:
    CROWDAI_EVENT_INFO="CROWDAI_EVENT_INFO"
    CROWDAI_EVENT_ERROR="CROWDAI_EVENT_ERROR"
    CROWDAI_EVENT_SUCCESS="CROWDAI_EVENT_SUCCESS"
    CROWDAI_EVENT_CODE_EXIT="CROWDAI_EVENT_CODE_EXIT"

    def __init__(self, with_oracle=False):
        self.IS_GRADING = os.getenv("CROWDAI_IS_GRADING", False)
        self.is_bootstrapped = False
        self.with_oracle = with_oracle #Marks if the communication is happenning with the oracle

        if self.IS_GRADING:
            self.AGENT_ID = os.getenv("CROWDAI_AGENT_ID", "undefined")
            self.REDIS_HOST = os.getenv("CROWDAI_REDIS_HOST", "localhost")
            self.REDIS_PORT = os.getenv("CROWDAI_REDIS_PORT", "6379")
            self.REDIS_DB = os.getenv("CROWDAI_REDIS_DB", 0)
            self.REDIS_PASSWORD = os.getenv("CROWDAI_REDIS_PASSWORD", False)
            self.REDIS_SOCKET_TIMEOUT = float(os.getenv("REDIS_SOCKET_TIMEOUT", 60))
            self.REDIS_SOCKET_CONNECT_TIMEOUT = float(os.getenv("REDIS_SOCKET_CONNECT_TIMEOUT", 60))
            self.REDIS_CALL_SLEEP_TIME = float(os.getenv("REDIS_CALL_SLEEP_TIME", 1))

            self.REDIS_COMMUNICATION_CHANNEL = \
                os.getenv(  "CROWDAI_REDIS_COMMUNICATION_CHANNEL",
                            "CROWDAI_REDIS_COMMUNICATION_CHANNEL"
                        )
            self.ORACLE_COMMUNICATION_CHANNEL = \
                os.getenv(  "CROWDAI_ORACLE_COMMUNICATION_CHANNEL",
                            "CROWDAI_ORACLE_COMMUNICATION_CHANNEL"
                        )

            self.BLOCKING_RESPONSE_CHANNEL = \
                os.getenv(  "CROWDAI_BLOCKING_RESPONSE_CHANNEL",
                            "CROWDAI_BLOCKING_RESPONSE_CHANNEL"
                        )

            self.REDIS_POOL = redis.ConnectionPool(
                                host=self.REDIS_HOST,
                                port=self.REDIS_PORT,
                                db=self.REDIS_DB
                                )
            # TODO: Add support for REDIS Password
            # TODO: Add tests

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        return self.get_event()

    def bootstrap(self):
        """
            Wait for a redis connection to appear if in
            grading mode
        """
        if self.IS_GRADING:
            if not self.is_bootstrapped:
                logger.debug("Waiting for redis connection...")
                while True:
                    try:
                        r = redis.Redis(connection_pool=self.REDIS_POOL,
                                        socket_timeout=self.REDIS_SOCKET_TIMEOUT,
                                        socket_connect_timeout=self.REDIS_SOCKET_CONNECT_TIMEOUT)
                        r.keys()
                        logger.debug("Established connection with redis server...")
                        self.is_bootstrapped = True
                        break
                    except redis.exceptions.ConnectionError:
                        time.sleep(self.REDIS_CALL_SLEEP_TIME)
                        continue

    def get_event(self):
        logger.debug("Attempting to GET crowdAI API Event ")
        self.bootstrap()
        if self.IS_GRADING:
            r = redis.Redis(connection_pool=self.REDIS_POOL,
                            socket_timeout=self.REDIS_SOCKET_TIMEOUT,
                            socket_connect_timeout=self.REDIS_SOCKET_CONNECT_TIMEOUT)

            if self.with_oracle:
                communication_channel = self.ORACLE_COMMUNICATION_CHANNEL
            else:
                communication_channel = self.REDIS_COMMUNICATION_CHANNEL

            while True:
                """
                    An indefinite/blocking wait until we receive a message
                """
                params = r.brpop(communication_channel)
                if params:
                    channel, data = params
                    logger.debug("Received crowdAI API Event {}".format(data))
                    if type(data) == bytes:
                        data = data.decode('utf-8')
                    return json.loads(data)
                else:
                    time.sleep(self.REDIS_CALL_SLEEP_TIME)
                    continue
        else:
            raise Exception("Attempting to GET event when CROWDAI_IS_GRADING is False")

    def send_blocking_call_response(self, response):
        response = json.dumps(response)
        r = redis.Redis(connection_pool=self.REDIS_POOL,
                        socket_timeout=self.REDIS_SOCKET_TIMEOUT,
                        socket_connect_timeout=self.REDIS_SOCKET_CONNECT_TIMEOUT)

        r.lpush(self.BLOCKING_RESPONSE_CHANNEL, response)

    def register_event(self, event_type, message="", payload={}, blocking=False):
        logger.debug("Registering crowdAI API Event : {} {} {} # with_oracle? : {}".format(
            event_type, message, payload, self.with_oracle
        ))
        self.bootstrap()
        if self.IS_GRADING:
            # TODO : Add validation
            _object = {}
            _object["event_type"] = event_type
            _object["agent_id"] = self.AGENT_ID
            _object["message"] = message
            _object["payload"] = payload
            r = redis.Redis(connection_pool=self.REDIS_POOL,
                            socket_timeout=self.REDIS_SOCKET_TIMEOUT,
                            socket_connect_timeout=self.REDIS_SOCKET_CONNECT_TIMEOUT)

            if self.with_oracle:
                communication_channel = self.ORACLE_COMMUNICATION_CHANNEL
            else:
                communication_channel = self.REDIS_COMMUNICATION_CHANNEL

            r.lpush(communication_channel, json.dumps(_object))
            if blocking:
                """
                    If blocking==True, then wait indefitely for an acknowledgement/response
                    from the grading infrastructure.
                    The response will be a valid json object.
                """
                while True:
                    """
                    An indefinite While loop to ensure the socket timeouts
                    dont interfere with the expected behaviour of the
                    blocking calls.
                    """
                    params = r.brpop(self.BLOCKING_RESPONSE_CHANNEL)
                    if params:
                        channel, data = params
                        if type(data) == bytes:
                            data = data.decode('utf-8')
                        acknowledgement = json.loads(data)
                        return acknowledgement
                    else:
                        time.sleep(self.REDIS_CALL_SLEEP_TIME)
                        continue
