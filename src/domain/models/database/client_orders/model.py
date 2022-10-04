from typing import List, Optional
from pydantic import BaseModel


class ClientOrdersModel(BaseModel):
    cl_order_id: Optional[str]
    account: Optional[str]
    time: Optional[int]
    quantity: Optional[int]
    average_price: Optional[int]
    price: Optional[int]
    last_price: Optional[int]
    stop_price: Optional[int]
    currency: Optional[str]
    symbol: Optional[str]
    side: Optional[str]
    status: Optional[str]
    tif: Optional[str]
    total_spent: Optional[float]
    quantity_filled: Optional[float]
    quantity_leaves: Optional[int]
    quantity_last: Optional[int]
    text: Optional[str]
    reject_reason: Optional[int]
    exec_type: Optional[str]
    expire_date: Optional[str]
    error_message: Optional[str]
