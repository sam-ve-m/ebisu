# standards
import logging
from typing import Optional, List, Dict, Type, Union

from fastapi import Request, Query
# Jormungandr
from heimdall_client.bifrost import Heimdall

from api.core.interfaces.interface import IService
from api.domain.enums.order_status import OrderStatus
from api.domain.enums.order_type import OrderType
from api.domain.enums.time_in_force import TIF
from api.domain.enums.trade_side import TradeSide
from api.repositories.oracle.repository import OracleRepository
from api.utils import utils

log = logging.getLogger()


def pipe_to_list(data: str):
    data = data.upper()
    list_data = data.split('|')
    return list_data


class GetOrders(IService):

    def __init__(
            self,
            symbols: str,
            order_type: Optional[OrderType],
            order_status: Optional[OrderStatus],
            trade_sides: Optional[TradeSide],
            time_in_forces: Optional[TIF],
            request: Request,

    ):
        self.symbols = pipe_to_list(symbols)
        self.order_type = order_type
        self.order_status = order_status
        self.trade_sides = trade_sides
        self.time_in_forces = time_in_forces
        self.jwt = request.headers.get("x-thebs-answer")
        if self.jwt is None:
            raise Exception('No token giving')
        heimdall = Heimdall(logger=log)
        jwt_data = heimdall.decrypt_payload(jwt=self.jwt)
        self.bovespa_account = jwt_data.get("bovespa_account")
        self.bmf_account = jwt_data.get("bmf_account")
        self.url_path = str(request.url)

    @staticmethod
    def decimal_128_converter(user_trade: dict, field: str) -> float:
        value = user_trade.get(field)
        if value:
            return float(value)
        return 0

    @staticmethod
    def normalize_open_order(user_trade: dict) -> dict:
        return {
            "account": user_trade.get("ACCOUNT"),
            "id": user_trade.get("CLORDID"),
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
            "total_spent": user_trade.get("CUMQTY") * GetOrders.decimal_128_converter(user_trade, "AVGPX"),
            "quantity_filled": user_trade.get("CUMQTY"),
            "quantity_leaves": user_trade.get("LEAVESQTY"),
            "quantity_last": user_trade.get("LASTQTY"),
            "text": user_trade.get("TEXT"),
            "reject_reason": user_trade.get("ORDREJREASON"),
            "exec_type": user_trade.get("EXECTYPE"),
            "expire_date": user_trade.get("EXPIREDATE"),
        }

    def get_service_response(self) -> List[dict]:
        open_orders = OracleRepository.instance()
        query = self.build_query()
        user_open_orders = open_orders.get_data(sql=query)
        return [
            GetOrders.normalize_open_order(user_open_order)
            for user_open_order in user_open_orders
        ]

    @staticmethod
    def create_filter(key: str, params: list):
        filter = f""" AND {key} IN {f"('{params[0]}')" if len(params) == 1 else str(tuple(params))}"""
        return filter

    def _organize_data(self) -> Dict[str, Union[List[str], OrderStatus, None, TradeSide, OrderType, TIF]]:
        data = {'symbol': self.symbols,
                'order_type': self.order_type,
                'order_status': self.order_status,
                'trade_sides': self.trade_sides,
                'time_in_forces': self.time_in_forces}

        return data

    def build_query(self) -> str:
        query = f"""SELECT * FROM UHYPEDB001.VW_CURRENT_EXECUTION_REPORTS WHERE ACCOUNT IN ('{self.bovespa_account}','{self.bmf_account}') """
        for key, value in self._organize_data.items():
            if value is None:
                continue
            value = [v.upper() for v in value]
            query += GetOrders.create_filter(
                utils.FROM_SEARCH_PARAMS_TO_ORACLE_KEYS[key],
                value
            )

        return query
