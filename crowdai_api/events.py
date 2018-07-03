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

    def __init__(self):
        self.IS_GRADING = os.getenv("CROWDAI_IS_GRADING", False)
        self.is_bootstrapped = False

        if self.IS_GRADING:
            self.AGENT_ID = os.getenv("CROWDAI_AGENT_ID", "undefined")
            self.REDIS_HOST = os.getenv("CROWDAI_REDIS_HOST", "localhost")
            self.REDIS_PORT = os.getenv("CROWDAI_REDIS_PORT", "6379")
            self.REDIS_DB = os.getenv("CROWDAI_REDIS_DB", 0)
            self.REDIS_PASSWORD = os.getenv("CROWDAI_REDIS_PASSWORD", False)
            self.REDIS_COMMUNICATION_CHANNEL = \
                os.getenv(  "CROWDAI_REDIS_COMMUNICATION_CHANNEL",
                            "CROWDAI_REDIS_COMMUNICATION_CHANNEL"
                        )

            self.REDIS_POOL = redis.ConnectionPool(
                                host=self.REDIS_HOST,
                                port=self.REDIS_PORT,
                                db=self.REDIS_DB
                                )
            # TODO: Add support for REDIS Password
            # TODO: Add tests

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
                        r = redis.Redis(connection_pool=self.REDIS_POOL)
                        r.keys()
                        logger.debug("Established connection with redis server...")
                        self.is_bootstrapped = True
                        break
                    except redis.exceptions.ConnectionError:
                        time.sleep(1)
                        continue



    def register_event(self, event_type, message="", payload={}):
        logger.debug("Received crowdAI API Event : {} {} {} ".format(
            event_type, message, payload
        ))
        self.bootstrap()
        if self.IS_GRADING:
            if event_type == self.CROWDAI_EVENT_CODE_EXIT:
                # Wait for 2 seconds to avoid race conditions
                # with other events
                import time
                time.sleep(2)
            
            # TODO : Add validation
            _object = {}
            _object["event_type"] = event_type
            _object["agent_id"] = self.AGENT_ID
            _object["message"] = message
            _object["payload"] = payload
            r = redis.Redis(connection_pool=self.REDIS_POOL)
            r.lpush(self.REDIS_COMMUNICATION_CHANNEL, json.dumps(_object))
