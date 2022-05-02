from enum import Enum

from etria_logger import Gladsheim
from fastapi import Query
from pydantic import BaseModel, Extra, ValidationError, root_validator
from api.domain.enums.region import Region
from api.exceptions.exceptions import BadRequestError


class BrokerNoteMarket(Enum):
    BMF = "bmf"
    BOVESPA = "bovespa"
    US = "us"

class ListBrokerNoteModel(BaseModel):
    region: Region
    market: BrokerNoteMarket
    year: int = Query(None)
    month: int = Query(None)

    @root_validator
    def validate_broker_note_properties(cls, broker_note_properties):
        market = broker_note_properties.get("market")
        region = broker_note_properties.get("region")

        br_markets = [BrokerNoteMarket.BMF, BrokerNoteMarket.BOVESPA]
        us_markets = [BrokerNoteMarket.US]

        is_valid_br_request = market in br_markets and region is Region.BR
        is_valid_us_request = market in us_markets and region is Region.US

        if not is_valid_br_request and not is_valid_us_request:
            message = f"Invalid combination to market:  {market} and region: {region}"
            Gladsheim.info(msg=message)
            raise BadRequestError(message)

        return broker_note_properties

    class Config:
        extra = Extra.forbid


