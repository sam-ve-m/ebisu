from strenum import StrEnum


class Balance(StrEnum):
    PROJECTED = "projected"
    ALLOWED_TO_TRADE = "allowed_to_trade"
    ALLOWED_TO_WITHDRAW = "allowed_to_withdraw"


class Wallet(StrEnum):
    BALANCE = "balance"
