from typing import List

from fastapi import APIRouter, Header

from libaccount.domains.me import Me
from libaccount.models.requestresponse.request import RegisterRequest, LoginRequest, UpdateProfileRequest
from libaccount.models.requestresponse.response import RegisterLoginResponse
from libshared.context import Context
from libshared.models.baserequestresponse import ErrorResponse
from libtrade.domains.trade import Trader
from libtrade.models.requestresponse.request import TradeRequest
from libtrade.models.requestresponse.response import TradeResponse

router = APIRouter()


@router.post(
    '/me/register',
    summary='Register a user',
    tags=['me'],
    response_model=RegisterLoginResponse,
    responses={403: {'model': ErrorResponse}},
)
async def register(payload: RegisterRequest):
    async with Context.tokenless():
        return await Me.register(payload=payload)


@router.post(
    '/me/login',
    summary='Login a user',
    tags=['me'],
    response_model=RegisterLoginResponse,
    responses={401: {'model': ErrorResponse}},
)
async def login(payload: LoginRequest):
    async with Context.tokenless():
        return await Me.login(payload=payload)


@router.put(
    '/me',
    summary='Update my profile',
    tags=['me'],
    response_model=RegisterLoginResponse,
    responses={401: {'model': ErrorResponse}},
)
async def update(payload: UpdateProfileRequest, authorization: str | None = Header(None)):
    async with Context.protected(authorization=authorization) as ctx:
        return await Me.update_profile(payload=payload, ctx=ctx)


@router.post(
    '/trades',
    summary='Post new trade',
    tags=['trades'],
    response_model=TradeResponse,
    responses={401: {'model': ErrorResponse}},
)
async def create_trade(payload: TradeRequest, authorization: str | None = Header(None)):
    async with Context.protected(authorization=authorization) as ctx:
        return await Trader.create_trade(payload=payload, ctx=ctx)


@router.get(
    '/trades',
    summary='Get my trades',
    tags=['trades'],
    response_model=List[TradeResponse],
    responses={401: {'model': ErrorResponse}},
)
async def my_trades(authorization: str | None = Header(None), since_id: str | None = None, size: int | None = None):
    async with Context.protected(authorization=authorization) as ctx:
        return await Trader.get_my_trades(ctx=ctx, since_id=since_id, size=size)
