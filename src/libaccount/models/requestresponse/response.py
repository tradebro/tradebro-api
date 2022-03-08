from __future__ import annotations

from libaccount.models.mongo import User
from libshared.models.baserequestresponse import BaseRequestResponse

from pydantic import HttpUrl, EmailStr


class RegisterLoginResponse(BaseRequestResponse):
    email: EmailStr

    display_name: str | None
    picture: HttpUrl | None

    access_token: str

    @classmethod
    def from_user(cls, user: User) -> RegisterLoginResponse:
        return RegisterLoginResponse(
            email=user.email, display_name=user.display_name, picture=user.picture, access_token=user.tokens[0].token
        )
