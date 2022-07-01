# STANDARD IMPORTS
from dataclasses import dataclass

# PROJECT IMPORTS
from src.domain.date_formatters.region.date_time.model import RegionStringDateTime


@dataclass(init=True)
class EarningBr:
    trade_history: str
    trade_type: str
    trade_code: str
    transaction_amount: float
    net_price: float
    date: RegionStringDateTime

    def get_date_in_time_stamp(self):
        timestamp = self.date.get_date_in_time_stamp()
        return timestamp

    def __repr__(self):
        earning_transaction = {
            "trade_history": self.trade_history,
            "trade_type": self.trade_type,
            "trade_code": self.trade_code,
            "transaction_amount": self.transaction_amount,
            "net_price": self.net_price,
            "date": self.date.get_date_in_time_stamp(),
        }

        return earning_transaction
