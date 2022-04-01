from pydantic import BaseModel
from fastapi import Request, Query
from api.domain.enums.region import Region


class ListClientOrder(BaseModel):
    request: Request
    region: Region
    limit: int
    offset: int
    order_status: str = Query(None)
