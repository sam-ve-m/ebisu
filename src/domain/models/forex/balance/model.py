from typing import List, Tuple, Union, NewType
from datetime import datetime

WithdrawValues = NewType(
    "WithdrawValues", List[Union[Tuple[Union[int, float], datetime.timestamp], None]]
)


class AllowedWithdraw:
    def __init__(self, withdraw_values: WithdrawValues):
        self.total = self.__get_total_total_available(withdraw_values=withdraw_values)

    @staticmethod
    def __get_total_total_available(withdraw_values) -> float:
        if not withdraw_values:
            return 0
        total_available = sum([value[0] for value in withdraw_values])
        return total_available
