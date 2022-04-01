from pydantic import BaseModel
from api.domain.enums.region import Region


class GetBalanceData(BaseModel):
    region: Region
