from fastapi import APIRouter, Request
import logging

from api.controller.base_controller import BaseController
from api.routers.validator.get_client_orders import SearchParams
from api.services.factories.get_client_orders import GetOrders

log = logging.getLogger()

router = APIRouter()


@router.get("get_client_orders_faas")
def get_client_orders(bmf_account: int, symbols: str, order_type: str, order_status: str, trade_sides: str,
                      time_in_forces: str, request: Request):
    validated_query = SearchParams(
        bmf_account=bmf_account,
        symbols=symbols,
        order_type=order_type,
        order_status=order_status,
        trade_sides=trade_sides,
        time_in_forces=time_in_forces
    )

    return BaseController.run(GetOrders, validated_query.dict(), request)