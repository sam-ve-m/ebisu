# STANDARD IMPORTS
from dataclasses import dataclass

# PROJECT IMPORTS
from src.domain.date_formatters.region.date_time.model import RegionStringDateTime


@dataclass(init=True)
class Earning:
    symbol: str
    description: str
    amount_per_share: float
    date: RegionStringDateTime
    amount: float

    def get_date_in_time_stamp(self):
        timestamp = self.date.get_date_in_timestamp_with_timezone_offset()
        return timestamp

    def __repr__(self):
        earning_transaction = {
            "symbol": self.symbol,
            "description": self.description,
            "amount_per_share": self.amount_per_share,
            "date": self.date.get_date_in_timestamp_with_timezone_offset(),
            "amount": self.amount,
        }

        return earning_transaction
