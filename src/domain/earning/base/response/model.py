# STANDARD IMPORTS
from datetime import datetime
from pydantic import BaseModel


class EarningsTransactionResponse(BaseModel):
    symbol: str
    name: str
    amount_per_share: float
    type: str
    tax_code: str
    date: int
