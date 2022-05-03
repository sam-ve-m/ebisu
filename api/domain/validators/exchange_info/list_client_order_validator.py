from typing import Optional
from pydantic import BaseModel
from fastapi import Query

from api.domain.enums.region import Region


class ListClientOrderModel(BaseModel):
    region: Region
    limit: int
    offset: int
    order_status: Optional[str] = Query(None)
