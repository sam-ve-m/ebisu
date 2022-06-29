# STANDARD IMPORTS
from dataclasses import dataclass

# PROJECT IMPORTS
from src.domain.date_formatters.region.date_time.model import RegionStringDateTime


@dataclass(init=True)
class Earning:
    symbol: str
    name: str
    amount_per_share: float
    type: str
    tax_code: str
    date: RegionStringDateTime

    def get_date_in_time_stamp(self):
        timestamp = self.date.get_date_in_time_stamp()
        return timestamp

    def __repr__(self):
        earning_transaction = {
            "symbol": self.symbol,
            "name": self.name,
            "amount_per_share": self.amount_per_share,
            "type": self.type,
            "tax_code": self.tax_code,
            "date": self.date,
        }

        return earning_transaction
