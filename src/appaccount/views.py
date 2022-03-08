from fastapi import APIRouter, Header

from libaccount.domains.me import Me
from libaccount.models.requestresponse.request import RegisterRequest, LoginRequest, UpdateProfileRequest
from libaccount.models.requestresponse.response import RegisterLoginResponse
from libaccount.context import Context

router = APIRouter()


@router.post('/me/register', summary='Register a user', tags=['me', 'register'], response_model=RegisterLoginResponse)
async def register_user(payload: RegisterRequest):
    async with Context.tokenless():
        return await Me.register(payload=payload)


@router.post('/me/login', summary='Login a user', tags=['me', 'login'], response_model=RegisterLoginResponse)
async def register_user(payload: LoginRequest):
    async with Context.tokenless():
        return await Me.login(payload=payload)


@router.put('/me', summary='Update my profile', tags=['me', 'update'], response_model=RegisterLoginResponse)
async def update_me(payload: UpdateProfileRequest, authorization: str | None = Header(None)):
    async with Context.protected(authorization=authorization) as ctx:
        return await Me.update_profile(payload=payload, ctx=ctx)
