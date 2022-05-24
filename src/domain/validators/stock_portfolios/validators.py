# STANDARD LIBS
from typing import Optional

from fastapi import Query
from pydantic import BaseModel

# EXTERNAL LIBS
from src.domain.enums.portfolios_classification import PortfolioClassification
from src.domain.enums.region import Region


class UserPortfoliosModel(BaseModel):
    region: Optional[Region] = Query(default=None)
    portfolio_classification: Optional[PortfolioClassification] = Query(default=None)
