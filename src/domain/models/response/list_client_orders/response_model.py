from typing import Optional, List
from pydantic import BaseModel
from src.domain.models.database.list_client_orders.model import ClientListOrdersModel


class ClientListOrdersResponse(BaseModel):
    name: Optional[str]
    cl_order_id: Optional[str]
    root_cl_order_id: Optional[str]
    time: Optional[float]
    quantity: Optional[int]
    order_type: Optional[str]
    average_price: Optional[int]
    currency: Optional[str]
    symbol: Optional[str]
    status: Optional[str]
    price: Optional[float]
    stop: Optional[str]
    side: Optional[str]
    total_spent: Optional[float]

    @classmethod
    def to_response(cls, models: List[ClientListOrdersModel]):
        orders = [
            ClientListOrdersResponse(
                name=model.name,
                cl_order_id=model.cl_order_id,
                root_cl_order_id=model.root_cl_order_id,
                time=model.time,
                quantity=model.quantity,
                order_type=model.order_type,
                average_price=model.average_price,
                currency=model.currency,
                symbol=model.symbol,
                status=model.status,
                price=model.price,
                stop=model.stop,
                side=model.side,
                total_spent=model.total_spent,
            ).dict()
            for model in models
        ]
        response = orders
        return response
