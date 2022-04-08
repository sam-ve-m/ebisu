from pydantic import BaseModel
from api.domain.enums.region import Region


class GetStatementModel(BaseModel):
    region: Region
    limit: int
    offset: int
    start_date: float
    end_date: float
