from pydantic import BaseModel
from api.domain.enums.region import Region


class GetClientOrderModel(BaseModel):
    region: Region
    cl_order_id: str
