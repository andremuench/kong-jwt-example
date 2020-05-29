class AuthIssueBaseException(Exception):
    pass


class ClientException(AuthIssueBaseException):
    pass


class UnauthorizedError(AuthIssueBaseException):
    pass

