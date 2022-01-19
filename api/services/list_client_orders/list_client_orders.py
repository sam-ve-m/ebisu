# standards
import logging
from fastapi import Request, Query, Response
from heimdall_client.bifrost import Heimdall
from orjson import orjson

from api.core.interfaces.interface import IService
from api.domain.enums.order_type import OrderType
from api.domain.enums.region import Region
from api.domain.enums.time_in_force import TIF
from api.domain.enums.trade_side import TradeSide
from api.services.list_client_orders.strategies import order_region
from api.utils.pipe_to_list import pipe_to_list

log = logging.getLogger()


class ListOrders(IService):
    mongo_singleton = None

    def __init__(
        self,
        request: Request,
        region: Region,
        symbols: str = Query(None),
        order_type: OrderType = Query(None),
        order_status: str = Query(None),
        trade_sides: TradeSide = Query(None),
        time_in_forces: TIF = Query(None),
    ):
        self.symbols = pipe_to_list(symbols)
        self.order_type = order_type
        self.order_status = pipe_to_list(order_status)
        self.trade_sides = trade_sides
        self.time_in_forces = time_in_forces
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
    async def normalize_open_order(user_trade: dict) -> dict:
        normalized_data = {
            "name": await ListOrders.get_name(user_trade.get('SYMBOL')),
            "cl_order_id": user_trade.get("CLORDID"),
            "time": user_trade.get("TRANSACTTIME"),
            "quantity": user_trade.get("ORDERQTY"),
            "average_price": ListOrders.decimal_128_converter(user_trade, "AVGPX"),
            "currency": "BRL",
            "symbol": user_trade.get("SYMBOL"),
            "status": user_trade.get("ORDSTATUS"),
            "total_spent": user_trade.get("CUMQTY")
            * ListOrders.decimal_128_converter(user_trade, "AVGPX"),
        }
        return normalized_data

    async def get_service_response(self) -> Response:
        self.get_account()
        open_orders = order_region[self.region]
        query = open_orders.build_query(self.bovespa_account, self.bmf_account, self.order_status)
        user_open_orders = open_orders.oracle_singleton_instance.get_data(sql=query)
        return Response(media_type="application/json", content=orjson.dumps([
            await ListOrders.normalize_open_order(user_open_order)
            for user_open_order in user_open_orders
        ]))

    @staticmethod
    async def get_name(symbol):
        name = await ListOrders.mongo_singleton.find_one({'symbol': symbol}, {'name': 1, '_id': 0})
        if not name:
            return
        return name.get('name')
