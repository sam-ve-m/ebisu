from typing import List, Optional
from pydantic import BaseModel


class ClientOrdersModel(BaseModel):
    cl_order_id: Optional[str]
    account: Optional[str]
    time: Optional[float]
    quantity: Optional[float]
    average_price: Optional[float]
    price: Optional[float]
    last_price: Optional[float]
    stop_price: Optional[float]
    currency: Optional[str]
    symbol: Optional[str]
    side: Optional[str]
    status: Optional[str]
    tif: Optional[str]
    total_spent: Optional[float]
    quantity_filled: Optional[float]
    quantity_leaves: Optional[float]
    quantity_last: Optional[float]
    text: Optional[str]
    reject_reason: Optional[int]
    exec_type: Optional[str]
    expire_date: Optional[float]
    error_message: Optional[str]
