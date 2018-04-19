# -*- coding: utf-8 -*-
import requests

"""Main module."""

class API:
    """
        API for
    """
    def __init__(self,
                authentication_token,
                grader_url="https://www.crowdai.org/api/external_graders/"):
        self.authentication_token = authentication_token
        self.grader_url = grader_url
        print("Working....")
