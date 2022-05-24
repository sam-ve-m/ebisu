from pydantic import BaseModel, Extra, validator, constr
from typing import Optional
from src.domain.enums.earnings_types import EarningsTypes
from src.domain.enums.region import Region


class EarningsClientModel(BaseModel):
    region: Region
    limit: int
    offset: int
    earnings_types: Optional[constr(min_length=1)]

    class Config:
        extra = Extra.forbid

    @validator("earnings_types")
    def validate_symbols(cls, e):
        if e:
            e = cls.pipe_to_list(e)
        return e

    @staticmethod
    def pipe_to_list(data):
        data = data.upper()
        list_data = data.split("|")
        earnings_types = [EarningsTypes[each_data.upper()] for each_data in list_data]
        return earnings_types
