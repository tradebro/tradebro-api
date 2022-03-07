from fastapi import APIRouter

from libaccount.domains.me import Me
from libaccount.models.requestresponse.request import RegisterRequest, LoginRequest
from libaccount.models.requestresponse.response import RegisterLoginResponse
from libaccount.context import Context

router = APIRouter()


@router.post('/me/register', summary='Register a user', tags=['me', 'register'], response_model=RegisterLoginResponse)
async def register_user(payload: RegisterRequest):
    async with Context():
        return await Me.register(payload=payload)


@router.post('/me/login', summary='Login a user', tags=['me', 'login'], response_model=RegisterLoginResponse)
async def register_user(payload: LoginRequest):
    async with Context():
        return await Me.login(payload=payload)
