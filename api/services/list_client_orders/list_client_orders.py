# Internal Lib
from typing import List
from fastapi import Query

from api.domain.enums.region import Region
from api.domain.validators.exchange_info_validators.list_client_order_validator import ListClientOrderModel
from api.repositories.companies_data.repository import CompanyInformationRepository
from api.services.list_client_orders.strategies import order_region
from api.domain.time_formatter.time_formatter import str_to_timestamp


class ListOrders:
    bmf_account = None
    bovespa_account = None
    company_information_repository = CompanyInformationRepository

    @classmethod
    def pipe_to_list(cls, data: str):
        list_data = None
        if isinstance(data, str):
            data = data.upper()
            list_data = data.split("|")
        return list_data

    @staticmethod
    def decimal_128_converter(user_trade: dict, field: str) -> float:
        value = user_trade.get(field)
        if value:
            return float(value)
        return 0

    @staticmethod
    async def normalize_open_order(user_trade: dict) -> dict:
        normalized_data = {
            "name": await ListOrders.company_information_repository.get_company_name(
                user_trade.get("SYMBOL")
            ),
            "cl_order_id": user_trade.get("CLORDID"),
            "time": str_to_timestamp(user_trade.get("TRANSACTTIME")),
            "quantity": user_trade.get("ORDERQTY"),
            "order_type": user_trade.get("ORDTYPE"),
            "average_price": ListOrders.decimal_128_converter(user_trade, "AVGPX"),
            "currency": "BRL",
            "symbol": user_trade.get("SYMBOL"),
            "status": user_trade.get("ORDSTATUS"),
            "total_spent": (user_trade.get("CUMQTY", float(0.0)) * ListOrders.decimal_128_converter(user_trade, "AVGPX")),

        }
        return normalized_data

    @classmethod
    async def get_service_response(cls,
                                   jwt_data: dict,
                                   list_client_orders: ListClientOrderModel
                                   ) -> List[dict]:
        user = jwt_data.get("user", {})
        portfolios = user.get("portfolios", {})
        br_portfolios = portfolios.get("br", {})
        cls.bovespa_account = br_portfolios.get("bovespa_account")
        cls.bmf_account = br_portfolios.get("bmf_account")

        open_orders = order_region[list_client_orders.region.value]

        order_status_res = ListOrders.pipe_to_list(list_client_orders.order_status)

        query = open_orders.build_query(
            bovespa_account=cls.bovespa_account,
            bmf_account=cls.bmf_account,
            offset=list_client_orders.offset,
            limit=list_client_orders.limit,
            order_status=order_status_res,
        )
        user_open_orders = open_orders.oracle_singleton_instance.get_data(sql=query)
        data = [
            await ListOrders.normalize_open_order(user_open_order)
            for user_open_order in user_open_orders
        ]
        if not data:
            return [{}]
        return data
