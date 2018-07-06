import json
from .helpers import make_api_call
from .exceptions import CrowdAIAPIException, CrowdAIRemoteException

class CrowdAISubmission:
    """Base Submission Class

        :param submission_id: crowdai submission_id
        :param grading_status: crowdai grading status. Can be one of -
                             ['submitted', 'initiated', 'graded', 'failed']
        :param message: crowdai grading message
        :param meta: meta key holding extra params related to the grading
    """
    def __init__(self,
                 score=False,
                 score_secondary=False,
                 submission_id=False,
                 grading_status="submitted",
                 message=False,
                 long_description=False,
                 meta={},
                 youtube_key=False,
                 image_key=False,
                 api_key=False,
                 auth_token=False,
                 challenge_id=False,
                 base_url="https://www.crowdai.org/api"):
        self.score = score
        self.score_secondary = score_secondary
        self.id = submission_id
        self.grading_status = grading_status
        self.message = message
        self.long_description = long_description
        self.meta = meta
        self.youtube_key = youtube_key
        self.image_key = image_key
        self.api_key = api_key
        self.auth_token = auth_token
        self.challenge_id = challenge_id
        self.round_id = False
        self.base_url = base_url

    def _serialize(self, meta_overwrite=True):
        """Serializes a submission object into an API compatible JSON

        :return json object
        :rtype dict
        """
        _object = {}

        if self.challenge_id is False:
            raise CrowdAIAPIException("Submission _serialize called without initialising challenge_id")

        if self.api_key is False:
            raise CrowdAIAPIException("Submission _serialize called without initialising participant api_key")

        _object["challenge_client_name"] = self.challenge_id
        if self.round_id:
            _object["challenge_round_id"] = self.round_id
        _object["api_key"] = self.api_key
        if self.score is not False:
            _object["score"] = self.score
            if self.score_secondary is False:
                raise CrowdAIAPIException("Score Secondary is null. \
The currrent API expects a token value for score secondary when score is set.")
            else:
                _object["score_secondary"] = self.score_secondary

        if self.grading_status not in ['submitted', 'initiated',
                                       'graded', 'failed']:
            raise CrowdAIAPIException("Submission _serialize called \
            with invalid grading status : {}".format(self.grading_status))

        _object["grading_status"] = self.grading_status
        if self.message:
            _object["grading_message"] = self.message

        if self.long_description:
            _object["description_markdown"] = self.long_description

        if self.youtube_key:
            _object["media_large"] = self.youtube_key
            _object["media_thumbnail"] = self.youtube_key
            _object["media_content_type"] = "video/youtube"

        if self.image_key:
            _object["media_large"] = self.image_key
            _object["media_thumbnail"] = self.image_key
            _object["media_content_type"] = "image/png"

        if len(self.meta.keys()) > 0:
            # Serialize JSON in a POST friendly way
            for _key in self.meta.keys():
                _object["meta[{}]".format(_key)] = self.meta[_key]
            if meta_overwrite:
                _object["meta_overwrite"] = True
        return _object

    def create_on_server(self):
        url = "{}/{}".format(self.base_url, "external_graders")
        _payload = self._serialize()
        response = make_api_call(self.auth_token,
                                 "post", url, payload=_payload)
        response_body = json.loads(response.text)
        if response.status_code == 202:
            submission_id = response_body["submission_id"]
            self.id = submission_id
        else:
            raise CrowdAIRemoteException(response_body["message"])

    def update(self, meta_overwrite=True):
        """Update the current submission object on the server
        """
        url = "{}/{}/{}".format(self.base_url,
                                "external_graders", self.id)
        _payload = self._serialize(meta_overwrite=meta_overwrite)
        response = make_api_call(self.auth_token,
                                 "patch", url, payload=_payload)
        response_body = json.loads(response.text)
        if response.status_code == 202:
            # Everything went well. Do nothing
            pass
        else:
            raise CrowdAIRemoteException(response_body["message"])

    def sync_with_server(self):
        """
        If a submission_id exists, then gets the latest values from the server
        and updates the relevant fields.
        """
        if self.id is False or self.challenge_id is False:
            raise CrowdAIAPIException("submission_id and challenge_id has \
            to be initialized before a sync_with_server operation \
            can complete.")

        url = "{}/{}/{}".format(self.base_url, "submissions",
                                self.id)
        response = make_api_call(self.auth_token, "get", url)
        if response.status_code is not 200:
            raise CrowdAIRemoteException("Invalid submission id")
        _submission_object = json.loads(response.text)
        # print("Response from server : ")
        # print(json.dumps(
        #     _submission_object,
        #     sort_keys=True,
        #     indent=4,
        #     separators=(',', ': ')
        # ))

        self.grading_status = _submission_object["grading_status_cd"]
        self.score = _submission_object["score"]
        self.score_secondary = _submission_object["score_secondary"]

        if "description_markdown" in _submission_object.keys():
            self.long_description = _submission_object["description_markdown"]


        if "meta" in _submission_object.keys():
            if type(_submission_object["meta"]) == dict:
                self.meta = _submission_object["meta"]
            else:
                try:
                    self.meta = json.loads(_submission_object["meta"])
                except Exception:
                    print(
                        "Received invalid meta key : {}, silently ignoring..."
                        .format(
                            _submission_object["meta"]
                            )
                        )

    def __repr__(self):
        def _template(key, value, tabfirst=True):
            response = ""
            if tabfirst:
                response += "\t"
            response += "{}\t:\t{}\n".format(key, value)
            return response

        string = ""
        string += "="*40 + "\n"
        string += _template("CrowdAISubmission",
                            self.id, tabfirst=False)
        string += _template("challenge_id", self.challenge_id)
        string += _template("round_id", self.round_id)
        string += _template("score", self.score)
        string += _template("score_secondary", self.score_secondary)
        string += _template("grading_status", self.grading_status)
        string += _template("message", self.message)
        if self.meta:
            string += _template("meta",
                                json.dumps(
                                    self.meta,
                                    sort_keys=True,
                                    indent=4,
                                    separators=(',', ': ')
                                ))
        string += "="*40 + "\n"
        return string

    def __str__(self):
        return self.__repr__()
