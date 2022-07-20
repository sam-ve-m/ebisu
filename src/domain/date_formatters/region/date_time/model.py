# STANDARD IMPORTS
from datetime import datetime, timedelta, timezone

# PROJECT IMPORTS
from src.domain.date_formatters.region.enum.date_format.enum import RegionDateFormat
from src.domain.date_formatters.region.enum.utc_offset.enum import ExchangeUtcOffset


class RegionStringDateTime:
    def __init__(
            self,
            date: datetime,
            utc_offset: ExchangeUtcOffset,
            region_date_format: RegionDateFormat
    ):
        self.__date = date
        self.__utc_offset = utc_offset
        self.__region_date_format = region_date_format

    def get_date_in_time_stamp_with_timezone_replace(self):
        timedelta_utc_offset = timedelta(minutes=self.__utc_offset.value)
        timezone_to_apply = timezone(timedelta_utc_offset)

        date_strptime = datetime.strptime(
            str(self.__date), self.__region_date_format.value
        )

        date_strptime = date_strptime.replace(tzinfo=timezone_to_apply)
        date_in_timestamp = date_strptime.timestamp() * 1000

        return int(date_in_timestamp)

    def get_date_in_timestamp_with_timezone_offset(self):
        timedelta_utc_offset = timedelta(minutes=self.__utc_offset.value)
        timezone_to_apply = timezone(timedelta_utc_offset)

        date_strptime = datetime.strptime(
            str(self.__date), self.__region_date_format.value
        )

        utc_datetime = date_strptime.astimezone(timezone_to_apply)
        utc_timestamp = datetime.timestamp(utc_datetime)
        date_in_timestamp = utc_timestamp * 1000

        return int(date_in_timestamp)
