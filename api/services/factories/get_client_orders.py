# standards
from datetime import datetime
import logging

# Third part
import yggdrasil_utils

# Jormungandr
from api.routers.validator.get_client_orders import SearchParams
from api.utils import utils

log = logging.getLogger()


class GetOrders:
    def __init__(self, params: SearchParams, url_path: str):
        self.params = params.dict()
        self.url_path = url_path

    def open_orders(self):
        cache = yggdrasil_utils.Cache.instance()
        yggdrasil_utils.EnumNormalizer.run(params=self.params)
        result = cache.get_or_create_cache(
            function_name=self.url_path,
            callback=GetOrders.run,
            callback_kwargs={"params": self.params},
            ttl=1,
        )
        return result

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

    @staticmethod
    def run(params: dict):
        open_orders = yggdrasil_utils.OracleRepository.instance()
        query = GetOrders.build_query(params=params)
        user_open_orders = open_orders.get_data(sql=query)
        return [
            GetOrders.normalize_open_order(user_open_order)
            for user_open_order in user_open_orders
        ]
    @staticmethod
    def create_filter(key: str, params: list):
        filter = f""" AND {key} IN {f"('{params[0]}')" if len(params) == 1 else str(tuple(params))}"""
        return filter

    @staticmethod
    def build_query(params: dict) -> str:
        query = f"""SELECT * FROM UHYPEDB001.VW_CURRENT_EXECUTION_REPORTS WHERE ACCOUNT IN ('{params['bovespa_account']}','{params['bmf_account']}') """
        del params['bovespa_account']
        del params['bmf_account']
        for key, value in params.items():
            if value is None:
                continue
            value = [v.upper() for v in value]
            query += GetOrders.create_filter(
                utils.FROM_SEARCH_PARAMS_TO_ORACLE_KEYS[key],
                value
            )

        return query

    def __call__(self, *args, **kwargs):
        return self.open_orders()
