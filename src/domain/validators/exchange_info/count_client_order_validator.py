from typing import Optional
from pydantic import BaseModel
from fastapi import Query

from src.domain.enums.region import Region


class GetClientOrderQuantityModel(BaseModel):
    region: Region
    order_status: Optional[str] = Query(None)
