# STANDARD IMPORTS
from pydantic import BaseModel


class TransactionResponse(BaseModel):
    date: int
    description: str
    value: float
