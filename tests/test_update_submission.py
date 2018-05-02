#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests api.get_submission."""

import os
import pytest

from crowdai_api import API as CROWDAI_API
from crowdai_api import CrowdAIRemoteException, CrowdAIAPIException

EXPECTED_KEYS = ['AUTH_TOKEN', 'EXAMPLE_API_KEY']
try:
    AUTH_TOKEN = os.environ["AUTH_TOKEN"]
    EXAMPLE_API_KEY = os.environ["EXAMPLE_API_KEY"]
except Exception as e:
    raise Exception("Environment variables do not seem to be set. "
                    + "Please set the following env variables: "
                    + ",".join(EXPECTED_KEYS)
                    )


def test_updates_submission():
    """Tests is it successfully updates submission"""
    api = CROWDAI_API(AUTH_TOKEN)
    challenge_id = "test_challenge"
    api.authenticate_participant(EXAMPLE_API_KEY)
    submission = api.create_submission(challenge_id)
    assert type(submission.id) == int
    assert submission.score is False
    assert submission.score_secondary is False
    assert submission.grading_status is "submitted"

    submission.score = 0.98
    submission.score_secondary = 0.99
    submission.grading_status = "graded"
    submission.update()

    submission_from_server = api.get_submission(challenge_id, submission.id)
    assert submission_from_server.score == 0.98
    assert submission_from_server.score_secondary == 0.99
    assert submission_from_server.grading_status == "graded"

def test_null_score_secondary_raises_exception():
    """Tests that an exception is raised when score is set and score_secondary
    is not.
    """

    api = CROWDAI_API(AUTH_TOKEN)
    challenge_id = "test_challenge"
    api.authenticate_participant(EXAMPLE_API_KEY)
    submission = api.create_submission(challenge_id)
    assert type(submission.id) == int
    assert submission.score is False
    assert submission.score_secondary is False
    assert submission.grading_status is "submitted"

    submission.score = 0.98
    submission.grading_status = "graded"
    with pytest.raises(CrowdAIAPIException):
        submission.update()
