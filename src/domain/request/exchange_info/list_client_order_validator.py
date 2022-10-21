from typing import Optional
from pydantic import BaseModel
from fastapi import Query

from src.domain.enums.region import Region
from src.domain.request.orders.order_status import OrderStatusValidator


class ListClientOrderModel(OrderStatusValidator):
    region: Region
    limit: int
    offset: int
