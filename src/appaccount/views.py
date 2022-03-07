from fastapi import APIRouter

from libaccount.domains.me import Me
from libaccount.models.requestresponse.request import RegisterRequest
from libaccount.models.requestresponse.response import RegisterResponse
from libaccount.context import Context

router = APIRouter()


@router.post('/me/register', summary='Register a user', tags=['me', 'register'], response_model=RegisterResponse)
async def register_user(payload: RegisterRequest):
    async with Context.tokenless():
        return await Me.register(payload=payload)
