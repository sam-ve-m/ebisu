from pydantic import BaseModel, Extra
from src.domain.enums.region import Region


class EarningsClientModel(BaseModel):
    cod_client: int
    region: Region
    limit: int
    offset: int

    class Config:
        extra = Extra.forbid
