from pydantic import BaseModel
from fastapi import Query
from api.domain.enums.region import Region


class ListBrokerNoteData(BaseModel):
    region: Region
    year: int = Query(None)
    month: int = Query(None)
