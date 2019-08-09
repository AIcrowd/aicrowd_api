#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests api.get_submission."""

import os
import pytest

from aicrowd_api import API as AICROWD_API
from aicrowd_api import AIcrowdRemoteException

EXPECTED_KEYS = ['AUTH_TOKEN', 'EXAMPLE_API_KEY']
try:
    AUTH_TOKEN = os.environ["AUTH_TOKEN"]
    EXAMPLE_API_KEY = os.environ["EXAMPLE_API_KEY"]
except Exception as e:
    raise Exception("Environment variables do not seem to be set. "
                    "Please set the following env variables : "
                    "" + (",".join(EXPECTED_KEYS))
                    )


def test_works_for_correct_submission_id():
    """Correct submission id returns a valid submission object"""
    api = AICROWD_API(AUTH_TOKEN)
    challenge_id = "test_challenge"
    submission_id = 6021
    submission = api.get_submission(challenge_id, submission_id)
    assert submission.id == submission_id
    assert submission.score == 10.1368634197571
    assert submission.score_secondary == 20.4264298439026
    assert submission.grading_status == "graded"
    print(submission)


def test_does_not_work_for_correct_submission_id():
    """Incorrect submission id throws an Exception"""
    api = AICROWD_API(AUTH_TOKEN)
    challenge_id = "test_challenge"
    submission_id = 9999999999
    with pytest.raises(AIcrowdRemoteException):
        api.get_submission(challenge_id, submission_id)
