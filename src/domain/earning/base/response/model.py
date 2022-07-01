# STANDARD IMPORTS
from pydantic import BaseModel


class EarningsTransactionResponse(BaseModel):
    symbol: str
    date: int
    amount_per_share: float
    description: str


class EarningsTransactionBrResponse(EarningsTransactionResponse):
    share_quantity: float
