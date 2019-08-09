#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests api.get_submission."""

import os
import pytest

from aicrowd_api import API as AICROWD_API
from aicrowd_api import AIcrowdRemoteException, AIcrowdAPIException

EXPECTED_KEYS = ['AUTH_TOKEN', 'EXAMPLE_API_KEY']
try:
    AUTH_TOKEN = os.environ["AUTH_TOKEN"]
    EXAMPLE_API_KEY = os.environ["EXAMPLE_API_KEY"]
except Exception as e:
    raise Exception("Environment variables do not seem to be set."
                    "Please set the following env variables: "
                    "" + (",".join(EXPECTED_KEYS))
                    )


def test_successfully_creates_submission_with_correct_api_key():
    """Tests if Successfully creates submission for correct api_key \
    and correct_challenge_id"""
    api = AICROWD_API(AUTH_TOKEN)
    challenge_id = "test_challenge"
    api.authenticate_participant(EXAMPLE_API_KEY)
    submission = api.create_submission(challenge_id)
    assert type(submission.id) == int
    assert submission.score is False
    assert submission.score_secondary is False
    assert submission.grading_status is "submitted"


def test_throws_error_when_not_authenticated():
    """Tests if throws error when creating submission without authentication"""
    api = AICROWD_API(AUTH_TOKEN)
    challenge_id = "test_challenge"
    with pytest.raises(AIcrowdAPIException):
        api.create_submission(challenge_id)


def test_throws_error_when_wrong_challenge_id():
    """Tests if throws error when creating submission with \
    wrong challenge id"""
    api = AICROWD_API(AUTH_TOKEN)
    api.authenticate_participant(EXAMPLE_API_KEY)
    challenge_id = "wrong_challenge_id"
    with pytest.raises(AIcrowdRemoteException):
        api.create_submission(challenge_id)
