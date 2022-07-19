from typing import List

from src.domain.enums.order_tifs import OrderTifs
from src.domain.validators.exchange_info.client_orders_validator import (
    GetClientOrderModel,
)
from src.services.get_client_orders.strategies import order_region
from src.domain.time_formatter.time_formatter import str_to_timestamp
from src.domain.enums.region import Region
from src.domain.currency_map.country_to_currency.map import country_to_currency


class GetOrders:
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
    def normalize_open_order(user_trade: dict, region: Region) -> dict:
        side = user_trade.get("SIDE")
        accumulated_quantity = user_trade.get("CUMQTY")
        currency = country_to_currency[region]

        normalized_data = {
            "cl_order_id": user_trade.get("CLORDID"),
            "account": user_trade.get("ACCOUNT"),
            "time": int(str_to_timestamp(user_trade.get("CREATEDAT")) * 1000),
            "quantity": user_trade.get("ORDERQTY"),
            "average_price": GetOrders.decimal_128_converter(user_trade, "AVGPX"),
            "price": GetOrders.decimal_128_converter(user_trade, "PRICE"),
            "last_price": GetOrders.decimal_128_converter(user_trade, "LASTPX"),
            "stop_price": GetOrders.decimal_128_converter(user_trade, "STOPPX"),
            "currency": currency.value,
            "symbol": user_trade.get("SYMBOL"),
            "side": side.lower() if side else side,
            "status": user_trade.get("ORDSTATUS"),
            "tif": GetOrders.tiff_response_converter(user_trade.get("TIMEINFORCE")),
            "total_spent": (
                (accumulated_quantity if accumulated_quantity else float(0.0))
                * GetOrders.decimal_128_converter(user_trade, "AVGPX")
            ),
            "quantity_filled": (
                accumulated_quantity if accumulated_quantity else float(0.0)
            ),
            "quantity_leaves": user_trade.get("LEAVESQTY"),
            "quantity_last": user_trade.get("LASTQTY"),
            "text": user_trade.get("TEXT"),
            "reject_reason": user_trade.get("ORDREJREASON"),
            "exec_type": user_trade.get("EXECTYPE"),
            "expire_date": int(str_to_timestamp(user_trade.get("EXPIREDATE")) * 1000) if user_trade.get("EXPIREDATE") else None,
            "error_message": user_trade.get("MESSAGE"),
        }
        return normalized_data

    @staticmethod
    def get_accounts_by_region(portfolios: dict, region: str) -> List[str]:
        accounts_by_region = {
            Region.BR.value: ["bovespa_account", "bmf_account"],
            Region.US.value: ["dw_id", "dw_account"],
        }
        fields = accounts_by_region[region]
        accounts = []
        for field in fields:
            if account := portfolios.get(field):
                accounts.append(account)
        return accounts

    @classmethod
    def get_service_response(
        cls, client_order: GetClientOrderModel, jwt_data: dict
    ) -> List[dict]:
        user = jwt_data.get("user", {})
        portfolios = user.get("portfolios", {})

        region = client_order.region.value
        region_portfolios = portfolios.get(region.lower(), {})

        accounts = cls.get_accounts_by_region(region_portfolios, region)

        open_orders = order_region[region]
        query = open_orders.build_query(
            accounts=accounts, clordid=client_order.cl_order_id
        )
        user_open_orders = open_orders.oracle_singleton_instance.get_data(sql=query)
        data = [
            GetOrders.normalize_open_order(user_open_order, client_order.region)
            for user_open_order in user_open_orders
        ]
        return data
