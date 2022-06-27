# STANDARD IMPORTS
import pytz
from datetime import datetime

# PROJECT IMPORTS
from src.domain.date_formatters.region.enum.date_format.enum import RegionDateFormat


class RegionTimeStamp:

    def __init__(
        self,
        timestamp: int,
        region_date_format: RegionDateFormat
    ):
        self.__timestamp = timestamp
        self.__region_date_format = region_date_format

    def get_region_string_datetime_from_timestamp(self):
        format_date = datetime.fromtimestamp(self.__timestamp / 1000).replace(tzinfo=pytz.utc)
        us_string_datetime = datetime.strftime(format_date, self.__region_date_format.value)
        return us_string_datetime

