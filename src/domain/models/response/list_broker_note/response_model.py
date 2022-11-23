from typing import Optional, List
from pydantic import BaseModel

from src.domain.models.database.list_broker_note.model import BrokerNoteModel


class ListBrokerNoteResponse(BaseModel):
    market: Optional[str]
    region: Optional[str]
    day: Optional[int]
    broker_note_link: Optional[str]

    @classmethod
    def to_response(cls, models: List[BrokerNoteModel]):
        broker_note = [
            ListBrokerNoteResponse(
                market=model.market,
                region=model.region,
                day=model.day,
                broker_note_link=model.broker_note_link,
            ).dict()
            for model in models
        ]
        response = broker_note
        return response
