from typing import Optional

from pydantic import BaseModel


class ResponseGetClientOrders(BaseModel):
    account: Optional[str]
    id: Optional[int]
    time: Optional[str]
    quantity: Optional[str]
    basis: Optional[str]
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
    reject_reason: Optional[str]
    exec_type: Optional[str]
    expire_date: Optional[str]