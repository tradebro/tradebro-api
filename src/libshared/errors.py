class TradebroGeneralError(Exception):
    code = 500
    message = 'Sorry, something wrong on our side'

    def __init__(self, code: int = code, message: str = message):
        self.code = code
        self.message = message


class NotFoundError(TradebroGeneralError):
    def __init__(self, message: str = 'The resource you requested is not found'):
        self.code = 404
        self.message = message


class UserNotFoundError(NotFoundError):
    def __init__(self, email: str):
        super().__init__(message=f'The email {email} is not found')


class ForbiddenError(TradebroGeneralError):
    def __init__(self, msg: str):
        self.code = 403
        self.message = msg


class UnauthorizedError(TradebroGeneralError):
    def __init__(self, message='The email and password combination is not recognized'):
        self.code = 401
        self.message = message
