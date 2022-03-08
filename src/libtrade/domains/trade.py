from libshared.context import Context
from libtrade.models.mongo import Trade
from libtrade.models.requestresponse.request import TradeRequest
from libtrade.models.requestresponse.response import TradeResponse


class Trader:
    @classmethod
    async def create_trade(cls, payload: TradeRequest, ctx: Context) -> TradeResponse:
        user_id = ctx.current_user.id

        trade = Trade.from_trade_request(payload=payload, user_id=user_id)
        await trade.save()

        return TradeResponse(**trade.dict())
