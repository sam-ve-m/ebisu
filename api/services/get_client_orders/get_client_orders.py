from typing import List

from api.domain.enums.order_tifs import OrderTifs
from api.domain.validators.exchange_info_validators.client_orders_validator import GetClientOrderModel
from api.services.get_client_orders.strategies import order_region
from api.domain.time_formatter.time_formatter import str_to_timestamp


class GetOrders:

    bmf_account = None
    bovespa_account = None

    @staticmethod
    def decimal_128_converter(user_trade: dict, field: str) -> float:
        value = user_trade.get(field)
        if value:
            return float(value)
        return 0

    @staticmethod
    def tiff_response_converter(tif_value: str):
        tiff_response = OrderTifs.has_member_value(value=tif_value)
        if tiff_response is not None:
            return tiff_response.value
        return OrderTifs.NOT_AVAILABLE.value

    @staticmethod
    def normalize_open_order(user_trade: dict) -> dict:
        side = user_trade.get("SIDE")

        normalized_data = {
            "cl_order_id": user_trade.get("CLORDID"),
            "account": user_trade.get("ACCOUNT"),
            "time": str_to_timestamp(user_trade.get("TRANSACTTIME")),
            "quantity": user_trade.get("ORDERQTY"),
            "average_price": GetOrders.decimal_128_converter(user_trade, "AVGPX"),
            "price": GetOrders.decimal_128_converter(user_trade, "PRICE"),
            "last_price": GetOrders.decimal_128_converter(user_trade, "LASTPX"),
            "stop_price": GetOrders.decimal_128_converter(user_trade, "STOPPX"),
            "currency": "BRL",
            "symbol": user_trade.get("SYMBOL"),
            "side": side.lower() if side else side,
            "status": user_trade.get("ORDSTATUS"),
            "tif": GetOrders.tiff_response_converter(user_trade.get("TIMEINFORCE")),
            "total_spent": user_trade.get("CUMQTY"),
            "quantity_filled": user_trade.get("CUMQTY"),
            "quantity_leaves": user_trade.get("LEAVESQTY"),
            "quantity_last": user_trade.get("LASTQTY"),
            "text": user_trade.get("TEXT"),
            "reject_reason": user_trade.get("ORDREJREASON"),
            "exec_type": user_trade.get("EXECTYPE"),
            "expire_date": user_trade.get("EXPIREDATE"),
            "error_message": user_trade.get("MESSAGE"),
        }
        return normalized_data

    @classmethod
    def get_service_response(cls, client_order: GetClientOrderModel, jwt_data: dict) -> List[dict]:
        user = jwt_data.get("user", {})
        portfolios = user.get("portfolios", {})
        br_portfolios = portfolios.get("br", {})
        cls.bovespa_account = br_portfolios.get("bovespa_account")
        cls.bmf_account = br_portfolios.get("bmf_account")
        region_value = client_order.region.value

        open_orders = order_region[region_value]
        query = open_orders.build_query(
            cls.bovespa_account, cls.bmf_account, clordid=client_order.cl_order_id
        )
        user_open_orders = open_orders.oracle_singleton_instance.get_data(sql=query)
        data = [
            GetOrders.normalize_open_order(user_open_order)
            for user_open_order in user_open_orders
        ]
        if not data:
            return [{}]
        return data
