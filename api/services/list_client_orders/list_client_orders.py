# standards
import logging
from typing import List

from fastapi import Request, Query, Depends

from api.application_dependencies.jwt_validator import jwt_validator_and_decompile
from api.core.interfaces.interface import IService
from api.domain.enums.region import Region
from api.services.list_client_orders.strategies import order_region
from api.utils.pipe_to_list import pipe_to_list
from api.utils.utils import str_to_timestamp
from api.domain.exception.model import DataNotFoundError


log = logging.getLogger()


class ListOrders(IService):
    mongo_singleton = None

    def __init__(
            self,
            request: Request,
            region: Region,
            limit: int,
            offset: int,
            order_status: str = Query(None),
            decompiled_jwt: dict = Depends(jwt_validator_and_decompile),
    ):
        self.order_status = pipe_to_list(order_status)
        self.jwt: dict = decompiled_jwt
        self.region = region.value
        self.offset = offset
        self.limit = limit
        self.bovespa_account = None
        self.bmf_account = None
        self.url_path = str(request.url)

    def get_account(self):
        user = self.jwt.get("user", {})
        portfolios = user.get("portfolios", {})
        br_portfolios = portfolios.get("br", {})
        self.bovespa_account = br_portfolios.get("bovespa_account")
        self.bmf_account = br_portfolios.get("bmf_account")

        self.bovespa_account = br_portfolios.get("user")
        self.bmf_account = br_portfolios.get("bmf_account")

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
            "time": str_to_timestamp(user_trade.get("TRANSACTTIME")),
            "quantity": user_trade.get("ORDERQTY"),
            "order_type": user_trade.get("ORDTYPE"),
            "average_price": ListOrders.decimal_128_converter(user_trade, "AVGPX"),
            "currency": "BRL",
            "symbol": user_trade.get("SYMBOL"),
            "status": user_trade.get("ORDSTATUS"),
            "total_spent": user_trade.get("CUMQTY")
                        * ListOrders.decimal_128_converter(user_trade, "AVGPX"),
        }
        return normalized_data

    async def get_service_response(self) -> List[dict]:
        self.get_account()
        open_orders = order_region[self.region]
        query = open_orders.build_query(bovespa_account=self.bovespa_account, bmf_account=self.bmf_account,
                                        offset=self.offset, limit=self.limit, order_status=self.order_status)
        user_open_orders = open_orders.oracle_singleton_instance.get_data(sql=query)
        return [
            await ListOrders.normalize_open_order(user_open_order)
            for user_open_order in user_open_orders
        ]

    @staticmethod
    async def get_name(symbol):
        name = await ListOrders.mongo_singleton.find_one({'symbol': symbol}, {'name': 1, '_id': 0})
        if not name:
            return [{}]
        return name.get('name')
