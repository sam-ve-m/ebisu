from enum import Enum


class OrderTifs(Enum):
    GOOD_TILL_CANCEL = "GTC"
    DAY = "DAY"
    IMMEDIATE_OR_CANCEL = "IOC"
    FILL_OR_KILL = "FOK"
    GOOD_TILL_DATE = "GTD"
    AT_THE_CLOSE = "ATC"
    GOOD_FOR_AUCTION = "GFA"
    NOT_AVAILABLE = "NA"

    @classmethod
    def has_member_value(cls, value):
        return cls.__members__.get(value)
