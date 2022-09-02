# Standards
from enum import IntEnum, Enum


class CurrencyOptions(Enum):
    BRL = "BRL"
    USD = "USD"


class NatureOperation(IntEnum):
    BRL_TO_USD = 4
    USD_TO_BRL = 54
