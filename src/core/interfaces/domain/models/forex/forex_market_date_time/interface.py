# Ebisu
from src.domain.enums.forex.liquidation_date import LiquidationDayOptions
from src.domain.enums.forex.time_zones import TimeZones

# Standards
from abc import ABC, abstractmethod
from datetime import datetime, date

# Third party
import pandas_market_calendars


class ForexMarketCalendars:
    def __init__(self):
        self.nyse = pandas_market_calendars.get_calendar("NYSE")
        self.bmf = pandas_market_calendars.get_calendar("BMF")


class ForexMarket(ABC):

    def __init__(self, date_time: datetime, time_zone: TimeZones):
        self.date_time = date_time
        self.date = date_time.date()
        self.time_zone = time_zone.value
        self.forex_calendar = ForexMarketCalendars()

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
