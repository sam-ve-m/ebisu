from src.domain.models.database.client_orders_quantity.model import QuantityModel
from typing import Optional
from pydantic import BaseModel


class QuantityResponse(BaseModel):
    quantity: Optional[int]

    @classmethod
    def to_response(cls, model: QuantityModel):
        quantity = model.quantity
        response = cls(quantity=quantity)
        return response
