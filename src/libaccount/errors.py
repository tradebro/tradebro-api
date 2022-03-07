class TradebroGeneralError(Exception):
    code = 500
    message = 'Sorry, something wrong on our side'

    def __init__(self, code: int = code, message: str = message):
        self.code = code
        self.message = message


class UserNotFoundError(TradebroGeneralError):
    def __init__(self, email: str):
        self.code = 404
        self.message = f'The user with the email {email} is not registered'


class ForbiddenError(TradebroGeneralError):
    def __init__(self, msg: str):
        self.code = 403
        self.message = msg


class UnauthorizedError(TradebroGeneralError):
    def __init__(self):
        self.code = 401
        self.message = f'The email and password combination is not recognized'
