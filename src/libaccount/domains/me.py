from libaccount.constants import TokenPurposes
from libaccount.errors import UserNotFoundError, ForbiddenError
from libaccount.models.mongo import User, Token
from libaccount.models.requestresponse.request import RegisterRequest
from libaccount.models.requestresponse.response import RegisterResponse


class Me:
    @classmethod
    async def register(cls, payload: RegisterRequest) -> RegisterResponse:
        user = await cls.get_user_by_email(email=payload.email)
        if user:
            raise ForbiddenError(f'The email {payload.email} is already registered')

        token = Token(purpose=TokenPurposes.Access.value)
        user = User(
            email=payload.email,
            password=User.password_hasher(password=payload.password1),
            display_name=payload.display_name,
            picture=payload.picture,
            tokens=[token]
        )
        await user.save()

        return RegisterResponse.from_user(user=user)

    @classmethod
    async def get_user_by_email(cls, email: str, raises_exception: bool = False):
        user = await User.find_one(User.email == email)
        if raises_exception and not user:
            raise UserNotFoundError(email=email)
        return user
