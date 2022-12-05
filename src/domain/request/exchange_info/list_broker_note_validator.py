# STANDARD LIBS
from enum import Enum

from pydantic import BaseModel, Extra, validator


class BrokerNoteMarket(Enum):
    BMF = "bmf"
    BOVESPA = "bovespa"
    US = "us"
    ALL = "all"


class BrokerNoteRegion(Enum):
    BR = "BR"
    US = "US"


class ListBrokerNoteBrModel(BaseModel):
    market: BrokerNoteMarket
    year: int
    month: int

    @validator("year")
    def validate_year(cls, value):
        if len(str(value)) < 4:
            raise ValueError("Year must be in format YYYY")
        return value

    @validator("month")
    def validate_month(cls, value):
        if (value < 1) or (value > 12):
            raise ValueError("Month must be an integer between 1 and 12")
        return value

    class Config:
        extra = Extra.forbid


class ListBrokerNoteUsModel(BaseModel):
    year: int
    month: int

    @validator("year")
    def validate_year(cls, value):
        if len(str(value)) < 4:
            raise ValueError("Year must be in format YYYY")
        return value

    @validator("month")
    def validate_month(cls, value):
        if (value < 1) or (value > 12):
            raise ValueError("Month must be an integer between 1 and 12")
        return value

    class Config:
        extra = Extra.forbid


class GetBrokerNoteUsModel(BaseModel):
    file_key: str

    class Config:
        extra = Extra.forbid
