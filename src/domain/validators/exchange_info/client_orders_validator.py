from pydantic import BaseModel
from src.domain.enums.region import Region


class GetClientOrderModel(BaseModel):
    region: Region
    root_cl_order_id: str
