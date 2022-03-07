from pydantic import EmailStr, HttpUrl

from tradebro.libshared.models.baserequestresponse import BaseRequestResponse


class RegisterRequest(BaseRequestResponse):
    email: EmailStr
    password1: str
    password2: str

    display_name: str | None
    picture: HttpUrl | None
