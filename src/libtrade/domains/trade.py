from typing import List

from beanie import PydanticObjectId

from libshared.context import Context
from libtrade.models.mongo import Trade
from libtrade.models.requestresponse.request import TradeRequest
from libtrade.models.requestresponse.response import TradeResponse


class Trader:
    @classmethod
    async def create_trade(cls, payload: TradeRequest, ctx: Context) -> TradeResponse:
        user_id = ctx.current_user.id

        trade = Trade(user_id=user_id, **payload.dict())
        await trade.save()

        return TradeResponse(**trade.dict())

    @classmethod
    async def get_my_trades(
        cls, *, ctx: Context, since_id: str | None = None, size: int | None = 10
    ) -> List[TradeResponse]:
        if not since_id:
            trades = await Trade.find(Trade.user_id == ctx.current_user.id).sort('-id').limit(size).to_list()
        else:
            trades = (
                await Trade.find(Trade.user_id == ctx.current_user.id, Trade.id <= PydanticObjectId(since_id))
                .sort('-id')
                .limit(size)
                .to_list()
            )

        return [TradeResponse(**x.dict()) for x in trades]
