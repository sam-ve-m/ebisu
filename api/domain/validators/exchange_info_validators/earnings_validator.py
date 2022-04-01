from pydantic import BaseModel


class GetEarningsData(BaseModel):
    symbol: str
    timestamp: float
    offset: float
    limit: int
