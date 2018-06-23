#!/usr/bin/env python
import os
import logging
import redis
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CrowdAIEvents:
    CROWDAI_EVENT_INFO="CROWDAI_EVENT_INFO"
    CROWDAI_EVENT_ERROR="CROWDAI_EVENT_ERROR"
    CROWDAI_EVENT_SUCCESS="CROWDAI_EVENT_SUCCESS"

    def __init__(self):
        self.IS_GRADING = os.getenv("CROWDAI_IS_GRADING", False)
        if self.IS_GRADING:
            self.REDIS_HOST = os.getenv("CROWDAI_REDIS_HOST", "localhost")
            self.REDIS_PORT = os.getenv("CROWDAI_REDIS_PORT", "6397")
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

    def register_event(self, event_type, message="", payload={}):
        logger.debug("Received crowdAI API Event : {} {} {} ".format(
            event_type, message, payload
        ))
        if self.IS_GRADING:
            # TODO : Add validation
            _object = {}
            _object["event_type"] = event_type
            _object["message"] = message
            _object["payload"] = payload
            r = redis.Redis(connection_pool=self.REDIS_POOL)
            r.lpush(self.REDIS_COMMUNICATION_CHANNEL, json.dumps(_object))
