from libaccount.constants import TokenPurposes
from libshared.context import Context
from libshared.errors import UserNotFoundError, ForbiddenError, UnauthorizedError
from libaccount.models.mongo import User, Token
from libaccount.models.requestresponse.request import RegisterRequest, LoginRequest, UpdateProfileRequest
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
            tokens=[token],
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

    @classmethod
    async def update_profile(cls, payload: UpdateProfileRequest, ctx: Context) -> RegisterLoginResponse:
        has_changes = False

        # Update display name
        if payload.display_name:
            ctx.current_user.display_name = payload.display_name
            has_changes = True

        # Update picture
        if payload.picture:
            ctx.current_user.picture = payload.picture
            has_changes = True

        # Update password
        if payload.password and payload.password1 and payload.password2:
            if payload.password1 == payload.password2:
                ctx.current_user.password = User.password_hasher(password=payload.password1)
                has_changes = True

        if has_changes:
            await ctx.current_user.save()

        return RegisterLoginResponse.from_user(user=ctx.current_user)
