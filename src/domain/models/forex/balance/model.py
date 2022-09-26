from typing import List, Tuple, Union, ByteString
from datetime import datetime


class AllowedWithdraw:
    def __init__(self, values: List[ByteString[Tuple[Union[int, float], datetime.timestamp]]]):
        self.total = self.__get_total_total_available(values=values)

    @staticmethod
    def __get_total_total_available(values) -> float:
        if not values:
            return 0
        values_decoded = [eval(value.decode()) for value in values]
        total_available = sum([value[0] for value in values_decoded])
        return total_available
