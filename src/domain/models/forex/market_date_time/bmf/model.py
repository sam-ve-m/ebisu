# Ebisu
from src.core.interfaces.domain.models.forex.forex_market_date_time.interface import ForexMarket
from src.domain.enums.forex.liquidation_date import LiquidationDayOptions

# Standards
from typing import List
from datetime import timedelta, date

# Third party
from decouple import config


class Bmf(ForexMarket):
    def __init__(self, date_time, time_zone):
        super().__init__(date_time, time_zone)

    async def validate_forex_business_day(self) -> bool:
        datetime_index = self.forex_calendar.bmf.valid_days(
            start_date=self.date,
            end_date=self.date,
            tz=self.time_zone
        )
        boolean = self.date in datetime_index
        return boolean

    async def validate_open_market_hours(self) -> bool:
        request_time = int(self.date_time.strftime("%H%M"))
        boolean = int(config("BMF_OPENING_TIME")) < request_time < int(config("BMF_CLOSING_TIME"))
        return boolean

    async def get_liquidation_date(self, day: LiquidationDayOptions) -> date:
        valid_dates = await self.get_range_dates()
        if self.date not in valid_dates:
            raise ExchangeMarketIsClosed
        liquidation_date = valid_dates[day.value]
        return liquidation_date

    async def get_range_dates(self) -> List[date]:
        end_date = self.date + timedelta(days=config("MARKET_DAYS_RANGE"))
        valid_dates = self.forex_calendar.bmf.valid_days(
            start_date=self.date,
            end_date=end_date,
            tz=self.time_zone
        )
        valid_dates_treated = [next_date for next_date in valid_dates.date]
        return valid_dates_treated
