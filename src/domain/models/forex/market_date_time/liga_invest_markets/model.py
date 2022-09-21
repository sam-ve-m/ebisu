# Ebisu
from src.core.interfaces.domain.models.forex.forex_market_date_time.interface import ForexMarket
from src.domain.enums.forex.liquidation_date import LiquidationDayOptions
from src.domain.enums.forex.time_zones import TimeZones
from src.domain.models.forex.market_date_time.nyse.model import Nyse
from src.domain.models.forex.market_date_time.bmf.model import Bmf

# Standards
from datetime import datetime, date

# Third party
from decouple import config


class LigaInvestStockMarket(ForexMarket):
    def __init__(self, date_time: datetime, time_zone: TimeZones):
        super().__init__(date_time, time_zone)
        self.nyse_market = Nyse(date_time=self.date_time, time_zone=self.time_zone)
        self.bmf_market = Bmf(date_time=self.date_time, time_zone=self.time_zone)

    async def validate_open_market_hours(self) -> bool:
        request_time = self.date_time.strftime("%H%M")
        boolean = int(config("LIGA_INVEST_OPENING_TIME")) < int(request_time) < int(config("LIGA_INVEST_CLOSING_TIME"))
        return boolean

    async def validate_forex_business_day(self) -> bool:
        bmf_valid_date = await self.bmf_market.validate_forex_business_day()
        nyse_valid_date = await self.nyse_market.validate_forex_business_day()
        boolean = bmf_valid_date and nyse_valid_date
        return boolean

    async def get_liquidation_date(self, day: LiquidationDayOptions) -> date:
        bmf_opening_dates = await self.bmf_market.get_range_dates()
        nyse_opening_dates = await self.nyse_market.get_range_dates()
        intersection_opening_dates = list(set(bmf_opening_dates) & set(nyse_opening_dates))
        if self.date not in intersection_opening_dates:
            raise ExchangeMarketIsClosed()
        liquidation_date = intersection_opening_dates[day.value]
        return liquidation_date
