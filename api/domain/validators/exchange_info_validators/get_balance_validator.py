from pydantic import BaseModel
from api.domain.enums.region import Region


class GetBalanceModel(BaseModel):
    region: Region
