class AIcrowdAPIException(Exception):
    def __init__(self, message, errors=[]):
        super(AIcrowdAPIException, self).__init__(message)
        self.errors = errors


class AIcrowdRemoteException(Exception):
    def __init__(self, message, errors=[]):
        super(AIcrowdRemoteException, self).__init__(message)
        self.errors = errors
