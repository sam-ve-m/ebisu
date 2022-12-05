from typing import Optional, List
from pydantic import BaseModel

from src.domain.models.database.list_broker_note.model import BrokerNoteModel


class ListBrokerNoteBrResponse(BaseModel):
    market: Optional[str]
    region: Optional[str]
    day: Optional[int]
    broker_note_link: Optional[str]

    @classmethod
    def to_response(cls, models: List[BrokerNoteModel]):
        broker_note = [
            ListBrokerNoteBrResponse(
                market=model.market,
                region=model.region,
                day=model.day,
                broker_note_link=model.broker_note_link,
            ).dict()
            for model in models
        ]
        response = broker_note
        return response


class ListBrokerNoteUsResponse(BaseModel):
    description: Optional[str]
    file_key: Optional[str]


class GetBrokerNoteUsResponse(BaseModel):
    broker_note_link: Optional[str]
