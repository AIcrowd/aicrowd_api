#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `crowdai_api` package."""

import os
import pytest
from crowdai_api import CrowdAIRemoteException
import uuid

from crowdai_api import API as CROWDAI_API
EXPECTED_KEYS = ['AUTH_TOKEN', 'EXAMPLE_API_KEY']
try:
    AUTH_TOKEN = os.environ["AUTH_TOKEN"]
    EXAMPLE_API_KEY = os.environ["EXAMPLE_API_KEY"]
except Exception as e:
    raise Exception("Environment variables do not seem to be set."
                    + "Please set the following env variables : "
                    + ",".join(EXPECTED_KEYS)
                    )


def test_valid_apikey_authenticates():
    """Tests if we can authenticate with valid API Key"""
    api = CROWDAI_API(AUTH_TOKEN)
    api.authenticate_participant(EXAMPLE_API_KEY)

    assert api.participant_id is not False


def test_invalid_apikey_doesnot_authenticates():
    """Tests : cannot authenticate with invalid API Key"""
    with pytest.raises(CrowdAIRemoteException):
        api = CROWDAI_API(AUTH_TOKEN)
        api.authenticate_participant(str(uuid.uuid4()))


def test_valid_api_authentication_with_username():
    """Tests if we can authenticate with valid username"""
    api = CROWDAI_API(AUTH_TOKEN)
    api.authenticate_participant_with_username("spMohanty")
    assert api.participant_id is not False


def test_error_on_authentication_with_wrong_username():
    """Tests if it throws error on authentication with wrong username"""
    with pytest.raises(CrowdAIRemoteException):
        api = CROWDAI_API(AUTH_TOKEN)
        api.authenticate_participant_with_username(str(uuid.uuid4()))
        assert api.participant_id is not False
