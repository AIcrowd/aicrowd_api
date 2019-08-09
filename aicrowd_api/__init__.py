# -*- coding: utf-8 -*-

"""Top-level package for AIcrowd API."""

__author__ = """S.P. Mohanty"""
__email__ = 'mohanty@aicrowd.com'
__version__ = '0.1.24'

from .aicrowd_api import API
from .submission import AIcrowdSubmission
from .events import AIcrowdEvents
from .exceptions import AIcrowdAPIException, AIcrowdRemoteException
