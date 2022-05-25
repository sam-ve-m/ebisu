from enum import Enum

from fastapi import Query
from pydantic import BaseModel, Extra


class BrokerNoteMarket(Enum):
    BMF = "bmf"
    BOVESPA = "bovespa"
    US = "us"
    ALL = "all"


class BrokerNoteRegion(Enum):
    BR = "BR"
    US = "US"
    ALL = "ALL"


class ListBrokerNoteModel(BaseModel):
    region: BrokerNoteRegion
    market: BrokerNoteMarket
    year: int = Query(None)
    month: int = Query(None)

    class Config:
        extra = Extra.forbid
