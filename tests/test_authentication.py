#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `crowdai_api` package."""

import os

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


def test_valid_api_authenticates():
    """Sample pytest test function with the pytest fixture as an argument."""
    api = CROWDAI_API(AUTH_TOKEN)
    is_valid_participant, participant_id, _ = \
        api.authenticate_participant(EXAMPLE_API_KEY)

    assert is_valid_participant is True
    assert type(participant_id) == int


def test_invalid_api_doesnot_authenticates():
    """Sample pytest test function with the pytest fixture as an argument."""
    api = CROWDAI_API(AUTH_TOKEN)
    is_valid_participant, participant_id, _ = \
        api.authenticate_participant(EXAMPLE_API_KEY)

    assert is_valid_participant is True
    assert type(participant_id) == int
