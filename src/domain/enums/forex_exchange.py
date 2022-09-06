# Standards
from enum import IntEnum
from strenum import StrEnum


class CurrencyOptions(StrEnum):
    BRL = "BRL"
    USD = "USD"


class NatureOperation(IntEnum):
    BRL_TO_USD = 4
    USD_TO_BRL = 54
