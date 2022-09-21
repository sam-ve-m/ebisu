# Ebisu
from src.domain.enums.forex_exchange.time_zones import TimeZones

# Standards
from abc import ABC, abstractmethod
from datetime import datetime

# Third party
import pandas_market_calendars as exchange_calendar


class ExchangeMarketCalendars:
    def __init__(self):
        self.nyse = exchange_calendar.get_calendar("NYSE")
        self.bmf = exchange_calendar.get_calendar("BMF")


class ExchangeMarket(ABC):

    def __init__(self, date_time: datetime, time_zone: TimeZones):
        self.date_time = date_time
        self.date = date_time.date()
        self.time_zone = time_zone
        self.exchange_calendar = ExchangeMarketCalendars()

    @abstractmethod
    async def validate_open_market_hours(self) -> bool:
        pass

    @abstractmethod
    async def validate_exchange_business_day(self) -> bool:
        pass

    @abstractmethod
    def get_next_d2_exchange_business_day(self):
        """This method must return next d2 exchange business date"""
        pass
