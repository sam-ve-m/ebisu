# Standards
from enum import Enum


class OrderType(Enum):
    TRADE = "TRADE"
    REJECTED = "REJECTED"
    OPEN = "OPEN"
    CANCELED = "CANCELED"
