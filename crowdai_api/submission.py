"""
Submission Class
"""


class CrowdAISubmission:
    """Base Submission Class

        :param submission_id: crowdai submission_id
        :param grading_status: crowdai grading status. Can be one of -
                             ['submitted', 'initiated', 'graded', 'failed']
        :param message: crowdai grading message
        :param meta: meta key holding extra params related to the grading
    """
    def __init__(self,
                 auth_token,
                 submission_id,
                 grading_status="submitted",
                 message={},
                 meta={},
                 base_url="https://www.crowdai.org/api"):
        self.submission_id = submission_id
        self.grading_status = grading_status
        assert self.grading_status in ['submitted', 'initiated',
                                       'graded', 'failed']

        self.message = message
        self.meta = meta
        self.auth_token = auth_token
        self.grader_url = grader_url

    def update(self):
        """
        REST CALL happens here
        """
