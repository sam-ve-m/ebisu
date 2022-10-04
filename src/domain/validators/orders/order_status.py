from typing import List, Optional

from pydantic import BaseModel, validator

from src.domain.enums.order_status import OrderStatus


class OrderStatusValidator(BaseModel):
    order_status: Optional[List[OrderStatus]]

    @validator("order_status", pre=True)
    def pipe_to_list(cls, data: str):
        list_data = None
        if isinstance(data, str):
            data = data.upper()
            list_data = data.split("|")
        if list_data is None:
            return []
        return [OrderStatus[status] for status in list_data]
