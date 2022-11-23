# Ebisu

from src.core.interfaces.domain.models.forex.markets.interface import ForexMarket
from src.domain.enums.forex.liquidation_date import LiquidationDayOptions

from src.domain.exceptions.domain.model.forex.model import ClosedForexOperations
from src.infrastructures.env_config import config

# Standards
from datetime import date
from typing import List


class LigaInvestStock(ForexMarket):
    def __init__(self, date_time, time_zone, market_calendar):
        super().__init__(date_time, time_zone, market_calendar)

    def validate_open_market_hours(self) -> bool:
        request_time = self.date_time.strftime("%H%M")
        boolean = (
            int(config("LIGA_INVEST_OPENING_TIME"))
            < int(request_time)
            < int(config("LIGA_INVEST_CLOSING_TIME"))
        )
        return boolean

    def validate_forex_business_day(self) -> bool:
        opening_date = self.get_valid_date_range(end_date=self.start_date)
        boolean = self.start_date in opening_date
        return boolean

    def get_liquidation_date(self, day: LiquidationDayOptions) -> date:
        intersection_opening_dates = self.get_valid_date_range(end_date=self.end_date)
        if self.start_date not in intersection_opening_dates:
            raise ClosedForexOperations()
        liquidation_date = intersection_opening_dates[day]
        return liquidation_date

    def get_valid_date_range(self, end_date: date) -> List[date]:
        bmf_opening_dates = self.forex_calendar.bmf.valid_days(
            start_date=self.start_date, end_date=end_date, tz=self.time_zone
        )
        nyse_opening_dates = self.forex_calendar.nyse.valid_days(
            start_date=self.start_date, end_date=end_date, tz=self.time_zone
        )
        bmf_valid_dates_treated = [next_date for next_date in bmf_opening_dates.date]
        nyse_valid_dates_treated = [next_date for next_date in nyse_opening_dates.date]
        intersection_opening_dates = sorted(
            list(set(nyse_valid_dates_treated) & set(bmf_valid_dates_treated))
        )
        return intersection_opening_dates

if __name__ == "__main__":
    from datetime import datetime
    from src.domain.enums.forex.time_zones import TimeZones
    from src.domain.models.forex.markets.calendar.model import ForexMarketCalendars

    from src.domain.date_formatters.region.enum.date_format.enum import RegionDateFormat

    a = LigaInvestStock(
        date_time=datetime.now(tz=TimeZones.BR_SP.value),
        time_zone=TimeZones.BR_SP,
        market_calendar=ForexMarketCalendars(nyse=True, bmf=True),
    )
    b = a.get_liquidation_date(LiquidationDayOptions.D2)
    print(b.strftime(
            RegionDateFormat.BR_DATE_ZULU_FORMAT.value
        ))