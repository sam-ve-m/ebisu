from typing import List, Optional
from pydantic import BaseModel


class QuantityModel(BaseModel):
    quantity: Optional[int]
