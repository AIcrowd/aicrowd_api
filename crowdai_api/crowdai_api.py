# -*- coding: utf-8 -*-
from .helpers import make_api_call
from .submission import CrowdAISubmission
from .exceptions import CrowdAIAPIException
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
            raise Exception(message)
            # TODO: Raise Exception
            print("Unable to authenticate : ", message)

        return self.participant_api_key


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

            return (True, participant_id, message)
        else:
            message = response_body["message"]
            return (False, False, message)

    def get_submission(self, submission_id):
        url = "{}/{}/{}".format(self.base_url, "submissions", submission_id)
        response = make_api_call(self.auth_token, "get", url)
        _submission_object = json.loads(response)
        print(response.text)

    def create_submission(self, challenge_id):
        submission = CrowdAISubmission()
        submission.api_key = self.participant_api_key
        submission.base_url = self.base_url
        submission.auth_token = self.auth_token
        submission.challenge_id = challenge_id

        submission.create_on_server()
        return submission
        # _payload = {}
        # _payload["challenge_client_name"] = challenge_id
        # _payload["api_key"] = self.participant_api_key
        # _payload["grading_status"] = "submitted"
        # _payload["meta"] = {}
        #
        # response = make_api_call(self.auth_token,
        #                          "post", url, payload=_payload)
        # response_body = json.loads(response.text)
        # if response.status_code == 202:
        #     submission_id = response_body["submission_id"]
        #     #submissions_remaining = response_body["submissions_remaining"]
        #     #message = response_body["message"]
        #     return submission_id
        # else:
        #     #message = response_body["message"]
        #
        #     # TODO raise exception
        #     return False


    def update_submission(self, submission_id):
        url = "{}/{}/{}".format(self.base_url, "external_graders", submission_id)
        _payload = {}
        _payload["challenge_client_name"] = "test_challenge"
        _payload["api_key"] = self.participant_api_key
        _payload["grading_status"] = "graded"
        _payload["score"] = 0.1
        _payload["score_secondary"] = 0.12
        _payload["meta"] = {}
        grader_logs = ""
        for k in range(1000):
            grader_logs+="aksjhdkahskjdhakshd  jkashdkhashkdhashdsa\n"
        _payload["meta"]["grader_logs"] = grader_logs
        _payload["meta"] = json.dumps(_payload["meta"])
        response = make_api_call(self.auth_token, "patch", url, payload=_payload)
        print(response.status_code)
        print(response.text)
