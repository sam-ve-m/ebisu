from dataclasses import dataclass
import time
from datetime import datetime

from src.domain.statement.model.region_date_format.enum import RegionDateFormat


@dataclass(init=True)
class Transaction:
    date: datetime
    description: str
    value: float
    region_date_format: RegionDateFormat

    def __get_date_in_time_stamp(self):
        date_strptime = time.strptime(str(self.date), self.region_date_format.value)
        return time.mktime(date_strptime)

    def __repr__(self):
        transaction = {
            "date": self.__get_date_in_time_stamp(),
            "description": self.description,
            "value": self.value
        }

        return transaction
