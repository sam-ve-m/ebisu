from dataclasses import dataclass


@dataclass(init=True)
class Position:
    symbol: str
    quantity: float

    def __repr__(self):
        earning_transaction = {
            "symbol": self.symbol,
            "quantity": self.quantity,
        }
        return earning_transaction
