from typing import List

from fastapi import APIRouter, Header

from libshared.context import Context
from libtrade.domains.trade import Trader
from libtrade.models.requestresponse.request import TradeRequest
from libtrade.models.requestresponse.response import TradeResponse

router = APIRouter()


@router.post('/trades', summary='Post new trade', tags=['trade', 'new'], response_model=TradeResponse)
async def new_trade(payload: TradeRequest, authorization: str | None = Header(None)):
    async with Context.protected(authorization=authorization) as ctx:
        return await Trader.create_trade(payload=payload, ctx=ctx)


@router.get('/trades', summary='Get my trades', tags=['trade', 'list'], response_model=List[TradeResponse])
async def my_trades(authorization: str | None = Header(None), since_id: str | None = None, size: int | None = None):
    async with Context.protected(authorization=authorization) as ctx:
        return await Trader.get_my_trades(ctx=ctx, since_id=since_id, size=size)
