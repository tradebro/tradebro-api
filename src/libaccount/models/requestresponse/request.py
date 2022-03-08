from pydantic import EmailStr, HttpUrl

from libshared.models.baserequestresponse import BaseRequestResponse


class RegisterRequest(BaseRequestResponse):
    email: EmailStr
    password1: str
    password2: str

    display_name: str | None
    picture: HttpUrl | None


class LoginRequest(BaseRequestResponse):
    email: EmailStr
    password: str


class UpdateProfileRequest(BaseRequestResponse):
    password: str | None
    password1: str | None
    password2: str | None

    display_name: str | None
    picture: HttpUrl | None
