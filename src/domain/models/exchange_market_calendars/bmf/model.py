from src.core.interfaces.domain.models.forex_exchange.exchange_market_date_time.interface import ExchangeMarket
from datetime import datetime, timedelta

from src.domain.enums.forex_exchange.time_zones import TimeZones


class ExchangeDateTimeBmf(ExchangeMarket):
    def __init__(self, date_time: datetime, time_zone: TimeZones):
        super().__init__(date_time, time_zone)

    async def validate_exchange_business_day(self) -> bool:
        datetime_index = self.exchange_calendar.bmf.valid_days(
            start_date=self.date,
            end_date=self.date,
            tz=self.time_zone
        )
        boolean = self.date in datetime_index
        return boolean

    async def validate_open_market_hours(self) -> bool:
        request_time = int(self.date_time.strftime("%H%M"))
        boolean = 859 < request_time < 1631
        return boolean

    def get_next_d2_exchange_business_day(self):
        valid_dates = self.get_range_dates()
        if self.date not in valid_dates:
            raise ExchangeMarketIsClosed
        liquidation_date = valid_dates[2]
        return liquidation_date

    def get_range_dates(self) -> list:
        end_date = self.date + timedelta(days=15)
        valid_dates = self.exchange_calendar.bmf.valid_days(
            start_date=self.date,
            end_date=end_date,
            tz=self.time_zone
        )
        valid_dates_treated = [next_date for next_date in valid_dates.date]
        return valid_dates_treated
