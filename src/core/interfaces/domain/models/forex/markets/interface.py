# Ebisu
from src.domain.enums.forex.liquidation_date import LiquidationDayOptions
from src.domain.enums.forex.time_zones import TimeZones
from src.domain.models.forex.markets.calendar.model import ForexMarketCalendars
from src.infrastructures.env_config import config

# Standards
from abc import ABC, abstractmethod
from datetime import datetime, date, timedelta


class ForexMarket(ABC):
    def __init__(
        self,
        date_time: datetime,
        time_zone: TimeZones,
        market_calendar: ForexMarketCalendars,
    ):
        self.date_time = date_time
        self.time_zone = time_zone.value
        self.start_date = date_time.date()
        self.end_date = self.start_date + timedelta(
            days=int(config("MARKET_DAYS_RANGE"))
        )
        self.forex_calendar = market_calendar

    @abstractmethod
    async def validate_open_market_hours(self) -> bool:
        """This method should return if the requested time is within the opening hours of the forex market"""
        pass

    @abstractmethod
    async def validate_forex_business_day(self) -> bool:
        """This method should return if it is an open forex market day"""
        pass

    @abstractmethod
    def get_liquidation_date(self, day: LiquidationDayOptions) -> date:
        """This method must return next d2 exchange business date"""
        pass
