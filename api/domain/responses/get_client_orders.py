from pydantic import BaseModel


class ResponseGetClientOrders(BaseModel):
    account: str
    id: int
    time: str
    quantity: str
    basis: str
    price: float
    last_price: float
    stop_price: float
    currency: str
    symbol: str
    side: str
    status: str
    tif: str
    total_spent: float
    quantity_filled: float
    quantity_leaves: float
    quantity_last: float
    text: str
    reject_reason: str
    exec_type: str
    expire_date: str