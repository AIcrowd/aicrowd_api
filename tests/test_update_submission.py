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
    raise Exception("Environment variables do not seem to be set. "
                    "Please set the following env variables: "
                    "" + (",".join(EXPECTED_KEYS))
                    )


def test_updates_submission():
    """Tests is it successfully updates submission"""
    api = AICROWD_API(AUTH_TOKEN)
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


def test_updates_submission_with_meta():
    """Tests is it successfully updates submission with the meta param"""
    api = AICROWD_API(AUTH_TOKEN)
    challenge_id = "test_challenge"
    api.authenticate_participant(EXAMPLE_API_KEY)
    submission = api.create_submission(challenge_id)
    assert type(submission.id) == int
    assert submission.score is False
    assert submission.score_secondary is False
    assert submission.grading_status is "submitted"
    assert submission.meta == {}

    submission.score = 0.98
    submission.score_secondary = 0.99
    submission.grading_status = "graded"
    submission.meta["something"] = "A"
    submission.meta["something_else"] = "B"
    submission.update()

    submission_from_server = api.get_submission(challenge_id, submission.id)
    assert submission_from_server.score == 0.98
    assert submission_from_server.score_secondary == 0.99
    assert submission_from_server.grading_status == "graded"
    assert submission_from_server.meta["something"] == "A"
    assert submission_from_server.meta["something_else"] == "B"

    submission.score = 0.198
    submission.score_secondary = 0.199
    submission.grading_status = "graded"
    submission.meta["something"] = "A_1"
    submission.meta["something_else"] = "B_1"
    submission.update()
    submission_from_server = api.get_submission(challenge_id, submission.id)
    assert submission_from_server.score == 0.198
    assert submission_from_server.score_secondary == 0.199
    assert submission_from_server.grading_status == "graded"
    assert submission_from_server.meta["something"] == "A_1"
    assert submission_from_server.meta["something_else"] == "B_1"

# This test fails right in the first block where the submission object on a new
# create submission mysteriously has the meta param assigned from the previous test
# This needs further investigation
#
# def test_updates_submission_with_meta_with_metaoverwrite_forced_False():
#     """ Tests is it successfully updates submission with the
#         meta_overwrite param = False
#     """
#     api = AICROWD_API(AUTH_TOKEN)
#     challenge_id = "test_challenge"
#     api.authenticate_participant(EXAMPLE_API_KEY)
#     submission = api.create_submission(challenge_id)
#     assert submission.meta == {}

    # assert type(submission_new.id) == int
    # assert submission_new.score is False
    # assert submission_new.score_secondary is False
    # assert submission_new.grading_status is "submitted"
    # assert submission_new.meta == {}

    # submission.score = 0.98
    # submission.score_secondary = 0.99
    # submission.grading_status = "graded"
    # submission.meta["something"] = "A"
    # submission.meta["something_else"] = "B"
    # submission.update(meta_overwrite=False)
    #
    # submission_from_server = api.get_submission(challenge_id, submission.id)
    # assert submission_from_server.score == 0.98
    # assert submission_from_server.score_secondary == 0.99
    # assert submission_from_server.grading_status == "graded"
    # assert submission_from_server.meta["something"] == "A"
    # assert submission_from_server.meta["something_else"] == "B"
    #
    # submission.score = 0.198
    # submission.score_secondary = 0.199
    # submission.grading_status = "graded"
    # submission.meta["something"] = "A_1"
    # submission.meta["something_else"] = "B_1"
    # submission.update(meta_overwrite=False)
    # submission_from_server = api.get_submission(challenge_id, submission.id)
    # assert submission_from_server.score == 0.198
    # assert submission_from_server.score_secondary == 0.199
    # assert submission_from_server.grading_status == "graded"
    # assert submission_from_server.meta["something"] == "A_1"
    # assert submission_from_server.meta["something_else"] == "B_1"


def test_null_score_secondary_raises_exception():
    """Tests that an exception is raised when score is set and score_secondary
    is not.
    """

    api = AICROWD_API(AUTH_TOKEN)
    challenge_id = "test_challenge"
    api.authenticate_participant(EXAMPLE_API_KEY)
    submission = api.create_submission(challenge_id)
    assert type(submission.id) == int
    assert submission.score is False
    assert submission.score_secondary is False
    assert submission.grading_status is "submitted"

    submission.score = 0.98
    submission.grading_status = "graded"
    with pytest.raises(AIcrowdAPIException):
        submission.update()
