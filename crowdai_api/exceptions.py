class CrowdAIAPIException(Exception):
    def __init__(self, message, errors):
        super(CrowdAIAPIException, self).__init__(message)
        self.errors = errors
