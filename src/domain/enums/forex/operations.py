# Standards
from enum import IntEnum

# Third party
from strenum import StrEnum


class NatureOperation(IntEnum):
    BRL_TO_USD = 68
    USD_TO_BRL = 167


class OperationType(StrEnum):
    BRL_TO_USD = "OUT"
    USD_TO_BRL = "IN"
