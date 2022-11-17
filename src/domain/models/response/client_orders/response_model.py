from typing import Optional, List
from pydantic import BaseModel
from src.domain.models.database.client_orders.model import ClientOrdersModel


class ClientOrdersResponse(BaseModel):
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

    @classmethod
    def to_response(cls, models: List[ClientOrdersModel]):
        orders = [
            ClientOrdersResponse(
                cl_order_id=model.cl_order_id,
                account=model.account,
                time=model.time,
                quantity=model.quantity,
                average_price=model.average_price,
                price=model.price,
                last_price=model.last_price,
                stop_price=model.stop_price,
                currency=model.currency,
                symbol=model.symbol,
                side=model.side,
                status=model.status,
                tif=model.tif,
                total_spent=model.total_spent,
                quantity_filled=model.quantity_filled,
                quantity_leaves=model.quantity_leaves,
                quantity_last=model.quantity_last,
                text=model.text,
                reject_reason=model.reject_reason,
                exec_type=model.exec_type,
                expire_date=model.expire_date,
                error_message=model.error_message,
            ).dict()
            for model in models
        ]
        response = orders
        return response
