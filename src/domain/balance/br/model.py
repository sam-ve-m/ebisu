from src.domain.balance.base.model import BaseBalance


class Balance(BaseBalance):
    def __init__(self, available_for_trade: float, available_for_withdraw: float):
        self.__available_for_trade: float = available_for_trade
        self.__available_for_withdraw: float = available_for_withdraw

    def has_balance(self):
        total = self.__available_for_trade + self.__available_for_withdraw
        has_balance = total != 0
        return has_balance

    def __repr__(self):
        earning_transaction = {
            "available_for_trade": self.__available_for_trade,
            "available_for_withdraw": self.__available_for_withdraw,
        }
        return earning_transaction
