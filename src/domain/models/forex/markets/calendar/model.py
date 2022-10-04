from src.domain.enums.forex.market_calendars import Market
import pandas_market_calendars


class ForexMarketCalendars:
    def __init__(self, nyse: bool = False, bmf: bool = False):
        self.nyse = self.get_nyse_calendar(market=nyse)
        self.bmf = self.get_bmf_calendar(market=bmf)

    @staticmethod
    def get_nyse_calendar(market: bool):
        if not market:
            return market
        return pandas_market_calendars.get_calendar(Market.NYSE)

    @staticmethod
    def get_bmf_calendar(market: bool):
        if not market:
            return market
        return pandas_market_calendars.get_calendar(Market.BMF)
