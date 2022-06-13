# Standards
from enum import Enum


class StatementType(Enum):
    ALL = "ALL"
    INFLOWS = "INFLOWS"
    OUTFLOWS = "OUTFLOWS"
    FUTURE = "FUTURE"
