from pydantic import BaseModel
from api.domain.enums.region import Region


class GetBrokerNoteData(BaseModel):
    region: Region
    year: str
    month: str
    day: str
