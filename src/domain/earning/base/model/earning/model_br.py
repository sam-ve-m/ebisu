# STANDARD IMPORTS
from dataclasses import dataclass

# PROJECT IMPORTS
from src.domain.date_formatters.region.date_time.model import RegionStringDateTime


@dataclass(init=True)
class EarningBr:
    symbol: str
    trade_history: str
    trade_type: float
    trade_code: str
    transaction_amount: str
    net_price: float
    date: RegionStringDateTime

    def __repr__(self):
        earning_transaction = {
            "symbol": self.symbol,
            "trade_history": self.trade_history,
            "trade_type": self.trade_type,
            "trade_code": self.trade_code,
            "transaction_amount": self.transaction_amount,
            "net_price": self.net_price,
            "date": self.date,
        }

        return earning_transaction
