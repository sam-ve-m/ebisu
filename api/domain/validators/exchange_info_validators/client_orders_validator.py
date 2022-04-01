from pydantic import BaseModel
from fastapi import Request
from api.domain.enums.region import Region


class GetClientOrder(BaseModel):
    request: Request
    region: Region
    cl_order_id: str
