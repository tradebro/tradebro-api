from datetime import datetime
from decimal import Decimal

from pydantic import HttpUrl

from libshared.models.baserequestresponse import BaseRequestResponse


class TradeRequest(BaseRequestResponse):
    exchange: str
    pair: str

    trade_snapshot: HttpUrl
    reason_for_entry: str | None
    reason_for_exit: str | None

    direction: str
    entry_price: Decimal
    exit_price: Decimal

    leverage: int | None
    pnl_in_percent: Decimal | None
    pnl_in_currency: Decimal | None

    entry_at: datetime
    exit_at: datetime
