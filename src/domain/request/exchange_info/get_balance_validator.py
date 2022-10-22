from pydantic import BaseModel
from src.domain.enums.region import Region


class GetBalanceModel(BaseModel):
    region: Region
