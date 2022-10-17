from src.domain.models.forex.markets.liga_invest_markets.model import LigaInvestStock
from src.domain.enums.forex.time_zones import TimeZones
from src.domain.exceptions.domain.forex.model import ClosedForexOperations
from src.domain.models.forex.markets.calendar.model import ForexMarketCalendars

# Standards
from datetime import datetime

# Third party
from pydantic import BaseModel, root_validator


class ForexExecution(BaseModel):
    proposal_simulation_token: str

    @root_validator(pre=True)
    def check_card_number_omitted(cls, values: dict):
        liga_stock_market = LigaInvestStock(
            date_time=datetime.now(tz=TimeZones.BR_SP.value),
            time_zone=TimeZones.BR_SP,
            market_calendar=ForexMarketCalendars(nyse=True, bmf=True),
        )

        is_valid_open_market_hours = liga_stock_market.validate_open_market_hours()
        if not is_valid_open_market_hours:
            raise ClosedForexOperations()

        is_valid_forex_business_day = liga_stock_market.validate_forex_business_day()
        if not is_valid_forex_business_day:
            raise ClosedForexOperations()

        values.update(liga_invest_stock_market=liga_stock_market)
        return values
