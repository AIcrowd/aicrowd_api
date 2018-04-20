# -*- coding: utf-8 -*-
from .helpers import make_api_call
# from .submissions import CrowdAISubmission
# from .exceptions import CrowdAIAPIException
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
                 round_id=1,
                 base_url="https://www.crowdai.org/api",
                 ):
        self.auth_token = auth_token
        self.base_url = base_url
        print("Working....")

    def get_participant_api_key(self, username):
        """Returns the API key of a participant given a crowdai username
        :Example:

        >>> api = API(auth_token)
        >>> api_key = api.get_participant_api_key("spmohanty")
        """
        url = "{}/{}/{}".format(self.base_url, "participants", username)
        r = make_api_call(self.auth_token, "get", url)
        # print(r.text)
        # print(r.url)
        return r

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
            return (True, participant_id, message)
        else:
            message = response_body["message"]
            return (False, False, message)

    def get_submission(self, submission_id):
        return submission_id

    def create_submission(self):
        return 1123

    def update_submission(self,
                          submission_id,
                          status,
                          message,
                          meta
                          ):
        print(submission_id)
        return submission_id
