from typing import List, Tuple, Union
from datetime import datetime


class AllowedWithdraw:
    def __init__(self, values: List[Union[Tuple[Union[int, float], datetime.timestamp], None]]):
        self.total = self.__get_total_total_available(values=values)

    @staticmethod
    def __get_total_total_available(values) -> float:
        if not values:
            return 0
        total_available = sum([value[0] for value in values])
        return total_available
