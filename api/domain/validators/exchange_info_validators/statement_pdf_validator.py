from pydantic import BaseModel
from api.domain.enums.region import Region


class ListClientOrder(BaseModel):
    region: Region
