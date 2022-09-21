#
from src.domain.models.forex.market_date_time.liga_invest_markets.model import LigaInvestStockMarket
from src.domain.enums.forex.time_zones import TimeZones
from src.domain.exceptions.domain.forex_exchange.exception import ClosedForexOperations

# Standards
from datetime import datetime

# Third party
from pydantic import BaseModel, validator


class ForexExecution(BaseModel):
    customer_exchange_token: str
    stock_market: LigaInvestStockMarket = LigaInvestStockMarket(
        date_time=datetime.now(tz=TimeZones.BR_SP.value),
        time_zone=TimeZones.BR_SP
    )

    @validator("stock_market")
    def in_forex_business_hours(cls, stock_market: LigaInvestStockMarket):
        boolean = stock_market.validate_open_market_hours()
        if not boolean:
            raise ClosedForexOperations

    @validator("stock_market")
    def in_forex_business_day(cls, stock_market: LigaInvestStockMarket):
        boolean = stock_market.validate_forex_business_day()
        if not boolean:
            raise ClosedForexOperations
