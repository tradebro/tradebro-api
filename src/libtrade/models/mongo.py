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

    class Collection:
        name = "trades"
