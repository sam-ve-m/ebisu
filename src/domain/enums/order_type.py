# Standards
from enum import Enum


class OrderType(Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP_LOSS = "STOP_LOSS"
    STOP_LIMIT = "STOP_LIMIT"
    MARKET_WITH_LEFTOVER_AS_LIMIT = "MARKET_WITH_LEFTOVER_AS_LIMIT"
