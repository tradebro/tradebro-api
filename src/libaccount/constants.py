from enum import Enum


class TokenPurposes(str, Enum):
    Access = 'access'
    ForgotPassword = 'forgot_password'
