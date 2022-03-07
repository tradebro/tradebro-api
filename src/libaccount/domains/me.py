from libaccount.constants import TokenPurposes
from libaccount.errors import UserNotFoundError, ForbiddenError, UnauthorizedError
from libaccount.models.mongo import User, Token
from libaccount.models.requestresponse.request import RegisterRequest, LoginRequest
from libaccount.models.requestresponse.response import RegisterLoginResponse


class Me:
    @classmethod
    async def register(cls, payload: RegisterRequest) -> RegisterLoginResponse:
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

        return RegisterLoginResponse.from_user(user=user)

    @classmethod
    async def get_user_by_email(cls, email: str, raises_exception: bool = False) -> User:
        user = await User.find_one(User.email == email)
        if raises_exception and not user:
            raise UserNotFoundError(email=email)
        return user

    @classmethod
    async def login(cls, payload: LoginRequest) -> RegisterLoginResponse:
        try:
            user = await cls.get_user_by_email(email=payload.email, raises_exception=True)
        except UserNotFoundError:
            raise UnauthorizedError()

        is_authenticated = User.verify_password(plain_password=payload.password, hashed_password=user.password)
        if not is_authenticated:
            raise UnauthorizedError()

        return RegisterLoginResponse.from_user(user=user)
