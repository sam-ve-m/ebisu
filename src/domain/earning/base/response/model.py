# STANDARD IMPORTS
from datetime import datetime
from pydantic import BaseModel

# PROJECT IMPORTS
from src.domain.date_formatters.region.date_time.model import RegionStringDateTime


class EarningsRecordResponse(BaseModel):
    symbol: str
    name: str
    amount_per_share: float
    type: str
    tax_code: str
    date: int
