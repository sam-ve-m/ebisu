# standards
import logging
from typing import Optional, List, Dict, Union

from fastapi import Request, Query, Response
from fastapi.responses import JSONResponse
# Jormungandr
from heimdall_client.bifrost import Heimdall
from orjson import orjson

from api.core.interfaces.interface import IService
from api.domain.enums.order_status import OrderStatus
from api.domain.enums.order_type import OrderType
from api.domain.enums.region import Region
from api.domain.enums.time_in_force import TIF
from api.domain.enums.trade_side import TradeSide
from api.services.get_client_orders.strategies import order_region
from api.utils import utils
from api.utils.pipe_to_list import pipe_to_list

log = logging.getLogger()


class GetOrders(IService):

    def __init__(
        self,
        request: Request,
        region: Region,
        cl_order_id: str,
    ):
        self.clorid = cl_order_id
        self.jwt = request.headers.get("x-thebs-answer")
        self.region = region.value
        self.bovespa_account = None
        self.bmf_account = None
        self.url_path = str(request.url)

    def get_account(self):
        heimdall = Heimdall(logger=log)
        jwt_data = heimdall.decrypt_payload(jwt=self.jwt)
        self.bovespa_account = jwt_data.get("bovespa_account")
        self.bmf_account = jwt_data.get("bmf_account")

    @staticmethod
    def decimal_128_converter(user_trade: dict, field: str) -> float:
        value = user_trade.get(field)
        if value:
            return float(value)
        return 0

    @staticmethod
    def normalize_open_order(user_trade: dict) -> dict:
        normalized_data = {
            "cl_order_id": user_trade.get("CLORDID"),
            "account": user_trade.get("ACCOUNT"),
            "time": user_trade.get("TRANSACTTIME"),
            "quantity": user_trade.get("ORDERQTY"),
            "basis": GetOrders.decimal_128_converter(user_trade, "AVGPX"),
            "price": GetOrders.decimal_128_converter(user_trade, "PRICE"),
            "last_price": GetOrders.decimal_128_converter(user_trade, "LASTPX"),
            "stop_price": GetOrders.decimal_128_converter(user_trade, "STOPPX"),
            "currency": "BRL",
            "symbol": user_trade.get("SYMBOL"),
            "side": user_trade.get("SIDE"),
            "status": user_trade.get("ORDSTATUS"),
            "tif": user_trade.get("TIMEINFORCE"),
            "total_spent": user_trade.get("CUMQTY")
            * GetOrders.decimal_128_converter(user_trade, "AVGPX"),
            "quantity_filled": user_trade.get("CUMQTY"),
            "quantity_leaves": user_trade.get("LEAVESQTY"),
            "quantity_last": user_trade.get("LASTQTY"),
            "text": user_trade.get("TEXT"),
            "reject_reason": user_trade.get("ORDREJREASON"),
            "exec_type": user_trade.get("EXECTYPE"),
            "expire_date": user_trade.get("EXPIREDATE"),
        }
        return normalized_data

    def get_service_response(self) -> Response:
        self.get_account()
        open_orders = order_region[self.region]
        query = open_orders.build_query(self.bovespa_account, self.bmf_account, self.clorid)
        user_open_orders = open_orders.oracle_singleton_instance.get_data(sql=query)
        return Response(media_type="application/json", content=orjson.dumps([
            GetOrders.normalize_open_order(user_open_order)
            for user_open_order in user_open_orders
        ]))

