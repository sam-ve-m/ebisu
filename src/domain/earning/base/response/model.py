# STANDARD IMPORTS
from pydantic import BaseModel


class EarningsTransactionResponse(BaseModel):
    symbol: str
    name: str
    amount_per_share: float
    type: str
    tax_code: str
    date: int


class EarningsTransactionBrResponse(BaseModel):
    symbol: str
    trade_history: str
    trade_type: float
    trade_code: str
    transaction_amount: str
    net_price: float
    date: int
