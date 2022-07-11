from typing import List

from src.domain.balance.base.model import BaseBalance
from src.domain.positions.model import Position


class AccountCloseSteps:

    def __init__(self, balance: BaseBalance, positions: List[Position], earnings: any, region: str):
        self.__balance: BaseBalance = balance
        self.__positions: List[Position] = positions
        self.__earnings: any = earnings
        self.__region: str = region

    def has_permission_to_close_account(self):
        status = [self.has_balance(), self.has_positions(), self.has_earnings()]
        has_permission_to_close_account = all(status)
        return has_permission_to_close_account

    def has_balance(self):
        return self.__balance.has_balance()

    def has_positions(self):
        has_positions = len(self.__positions) > 0
        return has_positions

    def has_earnings(self):
        payable_earnings = bool(self.__earnings.payable)
        record_date_earnings = bool(self.__earnings.record_date)
        has_earnings = payable_earnings or record_date_earnings
        return has_earnings

    def get_account_steps(self) -> dict:
        account_steps = {
            "balance": not self.has_balance(),
            "positions": not self.has_positions(),
            "earnings": not self.has_earnings(),
            "region": self.__region
        }

        return account_steps
