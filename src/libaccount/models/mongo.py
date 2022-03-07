from typing import List

from beanie import Document
from pydantic import HttpUrl, EmailStr, Field
from passlib.context import CryptContext

from libshared.models.mongo import BaseDatetimeMeta
from libshared.utils import generate_new_token


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token(BaseDatetimeMeta):
    purpose: str
    token: str = Field(default_factory=generate_new_token)


class User(Document, BaseDatetimeMeta):
    email: EmailStr
    password: str

    display_name: str | None
    picture: HttpUrl | None

    tokens: List[Token] = []

    @staticmethod
    def password_hasher(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    class Collection:
        name = "users"
