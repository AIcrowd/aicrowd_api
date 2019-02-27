# -*- coding: utf-8 -*-
from .helpers import make_api_call
from .submission import CrowdAISubmission
from .exceptions import CrowdAIAPIException, CrowdAIRemoteException
import json

__docformat__ = 'reStructuredText'
__author__ = 'S.P. Mohanty'

"""Main module."""

class API:
    """Base API class

    :param auth_token: Authentication Token from crowdAI
    :param base_url: Grader URL for API calls.
           Default value : https://www.crowdai.org/api/external_graders/
    """
    def __init__(self,
                 auth_token,
                 base_url="https://www.crowdai.org/api",
                 ):
        self.auth_token = auth_token
        self.base_url = base_url

        self.participant_api_key = False
        self.participant_id = False

    def authenticate_participant_with_username(self, username):
        """Returns the API key of a participant given a crowdai username
        :Example:

        >>> api = API(auth_token)
        >>> api_key = api.get_participant_api_key("spmohanty")
        """
        url = "{}/{}/{}".format(self.base_url, "participants", username)
        response = make_api_call(self.auth_token, "get", url)
        response_body = json.loads(response.text)
        if response.status_code == 200:
            self.participant_id = response_body["id"]
            self.participant_api_key = response_body["api_key"]
        else:
            message = response_body["message"]
            raise CrowdAIRemoteException(message)
        self.authenticate_participant(self.participant_api_key)

    def authenticate_participant(self, api_key):
        """Authenticate API key of a participant

        :return is_authenticated?, participant_id, message
                if is_authenticated == False, then participant_id is set as
                False
        :Example:

        >>> api = API(auth_token)
        >>> is_valid_participant, participant_id, message = \
                                    api.authenticate_participant(api_key)
        >>> assert is_valid_participant in [True, False]
        """
        url = "{}/{}/{}".format(self.base_url, "external_graders", api_key)
        response = make_api_call(self.auth_token, "get", url)
        response_body = json.loads(response.text)
        if response.status_code == 200:
            participant_id = int(response_body["participant_id"])
            message = response_body["message"]

            self.participant_api_key = api_key
            self.participant_id = participant_id
        else:
            message = response_body["message"]
            raise CrowdAIRemoteException(message)

    def get_all_submissions(self, challenge_id, grading_status="graded"):
        """Returns all submissions for a particular challenge id

        :param challenge_id challenge_client_name from the challenge
        :param grading_status ['submitted', 'initiated', 'graded', 'failed', "*"]
            When grading_status == False, all possible grading_status are allowed

        :return List of submission ids
        :Example:

        >>> api = API(auth_token)
        >>> challenge_id = "test_challenge"
        >>> submissions = api.get_all_submissions(challenge_id)
        >>> print(submissions)

        TODO: Write Tests for this call
        """
        assert grading_status in ['submitted', 'initiated', 'graded', 'failed', '*']
        url = "{}/{}".format(self.base_url, "submissions")
        payload = {}
        payload["challenge_client_name"] = challenge_id
        if grading_status != "*":
            payload["grading_status"] = grading_status
        response = make_api_call(self.auth_token, "get", url, payload=payload)
        response_body = json.loads(response.text)
        if response.status_code == 200:
            submission_ids = response_body
            return submission_ids
        else:
            message = response_body["message"]
            raise CrowdAIRemoteException(message)

    def get_submission(self, challenge_id, submission_id):
        submission = CrowdAISubmission(base_url=self.base_url)
        submission.api_key = self.participant_api_key
        submission.base_url = self.base_url
        submission.auth_token = self.auth_token
        submission.id = submission_id
        submission.challenge_id = challenge_id
        submission.sync_with_server()
        return submission

    def create_submission(self, challenge_id, round_id=False):
        submission = CrowdAISubmission(base_url=self.base_url)
        submission.api_key = self.participant_api_key
        submission.base_url = self.base_url
        submission.auth_token = self.auth_token
        submission.challenge_id = challenge_id
        submission.round_id = round_id

        submission.create_on_server()
        return submission
