# STANDARD IMPORTS
from datetime import datetime

# PROJECT IMPORTS
from src.domain.date_formatters.region.enum.date_format.enum import RegionDateFormat


class RegionStringDateTime:

    def __init__(
        self,
        date: datetime,
        region_date_format: RegionDateFormat
    ):
        self.__date = date
        self.__region_date_format = region_date_format

    def get_date_in_time_stamp(self):
        date_strptime = datetime.strptime(str(self.__date), self.__region_date_format.value)
        date_in_timestamp = int(date_strptime.timestamp() * 1000)
        return date_in_timestamp
