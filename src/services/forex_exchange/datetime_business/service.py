# Third party
import pandas_market_calendars as exchange_calendar
import pytz

# Standards
from datetime import datetime, timedelta, date


class DateTimeBusinessService:
    sao_paulo_timezone = pytz.timezone('America/Sao_Paulo')
    bmf_calendar = exchange_calendar.get_calendar("BMF")
    nyse_calendar = exchange_calendar.get_calendar("NYSE")

    @classmethod
    def full_validation_date_time(cls, date_time: datetime) -> bool:
        pass

    @staticmethod
    def validate_if_is_liga_invest_business_hours(date_time: datetime) -> bool:
        request_datetime = int(date_time.strftime("%H%M"))
        result = 859 < request_datetime < 1631
        return result

    @classmethod
    def validate_if_is_bmf_business_day(cls, date_time: datetime, ) -> bool:
        start_date = date_time.date()
        datetime_index = cls.bmf_calendar.valid_days(start_date=start_date, end_date=start_date, tz=cls.sao_paulo_timezone)
        result = start_date in datetime_index
        return result

    @classmethod
    def validate_if_is_nyse_business_day(cls, date_time: datetime) -> bool:
        start_date = date_time.date()
        datetime_index = cls.nyse_calendar.valid_days(start_date=start_date, end_date=start_date, tz=cls.sao_paulo_timezone)
        result = start_date in datetime_index
        return result

    @classmethod
    def get_next_d2_business_day(cls, date_time: datetime):
        start_date = date_time.date()
        nyse_range_dates = cls.get_range_dates(calendar=cls.nyse_calendar, date_time=date_time)
        bmf_range_dates = cls.get_range_dates(calendar=cls.bmf_calendar, date_time=date_time)
        intersection_dates_between_bmf_and_nyse = nyse_range_dates.intersection(bmf_range_dates)
        if start_date not in intersection_dates_between_bmf_and_nyse:
            raise IsNotBusinessDay

    @classmethod
    def get_range_dates(cls, calendar: exchange_calendar, date_time: datetime):
        start_date = date_time.date()
        end_date = start_date + timedelta(days=15)
        valid_days = calendar.valid_days(start_date=start_date, end_date=end_date, tz=cls.sao_paulo_timezone)
        set_range_dates = {next_date for next_date in valid_days.date}
        return set_range_dates

    # @staticmethod
    # def format_datetime(date_time: datetime):
    #     date_formatted = date_time.strftime("%Y-%m-%d")
    #     return date_formatted
    #
    # @classmethod
    # def get_intersection_business_days(cls, start_date: date, end_date: date) -> set:
    #     nyse_dates = cls.nyse_calendar.valid_days(start_date=start_date, end_date=end_date, tz=cls.sao_paulo_timezone)
    #     bmf_dates = cls.nyse_calendar.valid_days(start_date=start_date, end_date=end_date, tz=cls.sao_paulo_timezone)
    #     nyse_range_dates = {us_date for us_date in nyse_dates.date}
    #     bmf_range_dates = {br_date for br_date in bmf_dates.date}
    #     intersection_range_dates = nyse_range_dates.intersection(bmf_range_dates)
    #     return intersection_range_dates

