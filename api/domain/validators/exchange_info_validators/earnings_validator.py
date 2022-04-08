from pydantic import BaseModel


class GetEarningsModel(BaseModel):
    symbol: str
    timestamp: float
    offset: float
    limit: int
