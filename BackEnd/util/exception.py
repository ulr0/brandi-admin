class CustomError(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code


class ValidationError(CustomError):
    pass


class AlreadyExistError(CustomError):
    pass


class InvalidRequest(CustomError):
    pass


class ProcessingFailureError(CustomError):
    pass


class InvalidUserError(CustomError):
    pass


class InvalidAccessError(CustomError):
    pass


class LoginRequiredError(CustomError):
    pass


class UnauthorizedError(CustomError):
    pass


class InvalidParamError(CustomError):
    pass

class OffsetOutOfRangeError(CustomError):
    pass

class LimitOutOfRangeError(CustomError):
    pass

class ParamRequiredError(CustomError):
    pass