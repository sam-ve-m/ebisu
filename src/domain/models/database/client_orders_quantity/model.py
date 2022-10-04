from typing import Optional
from pydantic import BaseModel


class QuantityModel(BaseModel):
    quantity: Optional[int]
