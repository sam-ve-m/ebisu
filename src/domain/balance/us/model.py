from src.domain.balance.base.model import BaseBalance


class Balance(BaseBalance):

    def __init__(self, available_for_trade: float, available_for_withdraw: float, cash_balance: float):
        self.__available_for_trade: float = available_for_trade
        self.__available_for_withdraw: float = available_for_withdraw
        self.__cash_balance: float = cash_balance

    def has_balance(self):
        total = self.__available_for_trade + self.__available_for_withdraw + self.__cash_balance
        has_balance = total != 0
        return has_balance

    def __repr__(self):
        earning_transaction = {
            "available_for_trade": self.__available_for_trade,
            "available_for_withdraw": self.__available_for_withdraw,
            "cash_balance": self.__cash_balance,
        }
        return earning_transaction
