from typing import Optional
from pydantic import BaseModel


class ClientListOrdersModel(BaseModel):
    name: Optional[str]
    cl_order_id: Optional[str]
    root_cl_order_id: Optional[str]
    time: Optional[float]
    quantity: Optional[float]
    order_type: Optional[str]
    average_price: Optional[float]
    currency: Optional[str]
    symbol: Optional[str]
    status: Optional[str]
    price: Optional[float]
    stop: Optional[float]
    side: Optional[str]
    total_spent: Optional[float]
