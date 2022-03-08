from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from beanie import Document, PydanticObjectId
from pydantic import HttpUrl

from libtrade.models.requestresponse.request import TradeRequest
from src.libshared.models.mongo import BaseDatetimeMeta


class Trade(Document, BaseDatetimeMeta):
    user_id: PydanticObjectId
    exchange: str
    pair: str
    trade_snapshot: HttpUrl

    reason_for_entry: str | None
    reason_for_exit: str | None

    direction: str | None
    entry_price: Decimal | None
    exit_price: Decimal | None

    leverage: int | None
    pnl_in_percent: Decimal | None
    pnl_in_currency: Decimal | None

    entry_at: datetime | None
    exit_at: datetime | None

    @classmethod
    def from_trade_request(cls, payload: TradeRequest, user_id: PydanticObjectId) -> Trade:
        return Trade(
            user_id=user_id,
            exchange=payload.exchange,
            pair=payload.pair,
            trade_snapshot=payload.trade_snapshot,
            reason_for_entry=payload.reason_for_entry,
            reason_for_exit=payload.reason_for_exit,
            direction=payload.direction,
            entry_price=payload.entry_price,
            exit_price=payload.exit_price,
            leverage=payload.leverage,
            pnl_in_percent=payload.pnl_in_percent,
            pnl_in_currency=payload.pnl_in_currency,
            entry_at=payload.entry_at,
            exit_at=payload.exit_at,
        )

    class Collection:
        name = "trades"
