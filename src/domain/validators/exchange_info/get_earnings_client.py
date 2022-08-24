# STANDARD IMPORTS
from datetime import datetime

from etria_logger import Gladsheim
from pydantic import BaseModel, Extra, validator, constr
from typing import Optional

# PROJECT IMPORTS
from src.domain.enums.earnings_types import EarningsTypes
from src.domain.enums.region import Region


class EarningsClientModel(BaseModel):
    region: Region
    limit: datetime = None
    offset: datetime = None
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
        try:
            data = data.upper()
            list_data = data.split("|")
            earnings_types = [EarningsTypes[each_data.upper()] for each_data in list_data]
            return earnings_types
        except Exception as e:
            Gladsheim.error(error=e, message=f"earnings_types must be one of the follow options {[str(earning_type.name) for earning_type in EarningsTypes]}")
