# STANDARD IMPORTS
from dataclasses import dataclass

# PROJECT IMPORTS
from src.domain.date_formatters.region.date_time.model import RegionStringDateTime


@dataclass(init=True)
class EarningBr:
    share_quantity: float
    symbol: str
    date: RegionStringDateTime
    description: str
    amount_per_share: float

    def get_date_in_time_stamp(self):
        timestamp = self.date.get_date_in_time_stamp()
        return timestamp

    def __repr__(self):
        earning_transaction = {
            "share_quantity": self.share_quantity,
            "symbol": self.symbol,
            "date": self.date.get_date_in_time_stamp(),
            "description": self.description,
            "amount_per_share": self.amount_per_share
        }

        return earning_transaction
