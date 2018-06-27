# -*- coding: utf-8 -*-

"""Top-level package for crowdAI API."""

__author__ = """S.P. Mohanty"""
__email__ = 'spmohanty91@gmail.com'
__version__ = '0.1.0'

from .crowdai_api import API
from .submission import CrowdAISubmission
from .gitlab_submission import GitlabSubmission
from .events import CrowdAIEvents
from .exceptions import *

import atexit
def exit_handler():
    crowdai_events = CrowdAIEvents()
    crowdai_events.register_event(
        event_type=CrowdAIEvents.CROWDAI_EVENT_CODE_EXIT
    )
atexit.register(exit_handler)
