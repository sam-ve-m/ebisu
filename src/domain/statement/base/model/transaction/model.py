# STANDARD IMPORTS
from dataclasses import dataclass

# PROJECT IMPORTS
from src.domain.date_formatters.region.date_time.model import RegionStringDateTime


@dataclass(init=True)
class Transaction:
    date: RegionStringDateTime
    description: str
    value: float

    def __repr__(self):
        transaction = {
            "date": self.date.get_date_in_time_stamp(),
            "description": self.description,
            "value": self.value,
        }

        return transaction
