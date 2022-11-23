from typing import Optional
from pydantic import BaseModel


class BrokerNoteModel(BaseModel):
    market: Optional[str]
    region: Optional[str]
    day: Optional[int]
    broker_note_link: Optional[str]