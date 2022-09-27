# Ebisu
from src.core.interfaces.domain.models.forex.markets.interface import ForexMarket
from src.domain.enums.forex.liquidation_date import LiquidationDayOptions
from src.domain.exceptions.domain.forex.exception import ClosedForexOperations

# Standards
from typing import List
from datetime import date

# Third party
from decouple import config


class Nyse(ForexMarket):
    def __init__(self, date_time, time_zone, market_calendar):
        super().__init__(date_time, time_zone, market_calendar)

    def validate_forex_business_day(self) -> bool:
        valid_dates = self.get_valid_date_range(end_date=self.start_date)
        boolean = self.start_date in valid_dates
        return boolean

    def validate_open_market_hours(self) -> bool:
        request_time = int(self.date_time.strftime("%H%M"))
        boolean = int(config("NYSE_OPENING_TIME")) < request_time < int(config("NYSE_CLOSING_TIME"))
        return boolean

    def get_liquidation_date(self, day: LiquidationDayOptions) -> date:
        valid_dates = self.get_valid_date_range(end_date=self.end_date)
        if self.start_date not in valid_dates:
            raise ClosedForexOperations()
        liquidation_date = valid_dates[day]
        return liquidation_date

    def get_valid_date_range(self, end_date: date) -> List[date]:
        valid_dates = self.forex_calendar.nyse.valid_days(
            start_date=self.start_date,
            end_date=end_date,
            tz=self.time_zone
        )
        valid_dates_treated = [next_date for next_date in valid_dates.date]
        return valid_dates_treated
