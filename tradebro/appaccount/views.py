from fastapi import APIRouter

from tradebro.libaccount.domains.me import Me
from tradebro.libaccount.models.requestresponse.request import RegisterRequest
from tradebro.libaccount.models.requestresponse.response import RegisterResponse
from tradebro.libaccount.context import Context

router = APIRouter()


@router.post('/me/register', summary='Register a user', tags=['me', 'register'], response_model=RegisterResponse)
async def register_user(payload: RegisterRequest):
    async with Context.tokenless():
        return await Me.register(payload=payload)
