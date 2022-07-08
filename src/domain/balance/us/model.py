from dataclasses import dataclass


@dataclass(init=True)
class Balance:
    available_for_trade: float
    available_for_withdraw: float
    cash_balance: float

    def __repr__(self):
        earning_transaction = {
            "available_for_trade": self.available_for_trade,
            "available_for_withdraw": self.available_for_withdraw,
            "cash_balance": self.cash_balance,
        }
        return earning_transaction
