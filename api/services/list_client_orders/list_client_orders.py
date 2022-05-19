# Internal Lib
from typing import List
from fastapi import Query

from api.domain.enums.region import Region
from api.domain.validators.exchange_info.list_client_order_validator import ListClientOrderModel
from api.repositories.companies_data.repository import CompanyInformationRepository
from api.services.list_client_orders.strategies import order_region
from api.domain.time_formatter.time_formatter import str_to_timestamp
from api.domain.currency_map.country_to_currency.map import country_to_currency
from api.domain.enums.order_status import OrderStatus


class ListOrders:
    company_information_repository = CompanyInformationRepository

    @classmethod
    def pipe_to_list(cls, data: str):
        list_data = None
        if isinstance(data, str):
            data = data.upper()
            list_data = [OrderStatus[status] for status in data.split("|")]
        return list_data

    @staticmethod
    def decimal_128_converter(user_trade: dict, field: str) -> float:
        value = user_trade.get(field)
        if value:
            return float(value)
        return 0

    @staticmethod
    async def normalize_open_order(user_trade: dict, region: Region) -> dict:
        currency = country_to_currency[region]
        accumulated_quantity = user_trade.get("CUMQTY")
        normalized_data = {
            "name": await ListOrders.company_information_repository.get_company_name(
                user_trade.get("SYMBOL")
            ),
            "cl_order_id": user_trade.get("CLORDID"),
            "time": str_to_timestamp(user_trade.get("TRANSACTTIME")),
            "quantity": user_trade.get("ORDERQTY"),
            "order_type": user_trade.get("ORDTYPE"),
            "average_price": ListOrders.decimal_128_converter(user_trade, "AVGPX"),
            "currency": currency.value,
            "symbol": user_trade.get("SYMBOL"),
            "status": user_trade.get("ORDSTATUS"),
            "total_spent": (
                (accumulated_quantity if accumulated_quantity else float(0.0))
                * ListOrders.decimal_128_converter(user_trade, "AVGPX")
            ),
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
    async def get_service_response(
        cls,
        jwt_data: dict,
        list_client_orders: ListClientOrderModel
    ) -> List[dict]:
        user = jwt_data.get("user", {})
        portfolios = user.get("portfolios", {})

        region = list_client_orders.region.value
        region_portfolios = portfolios.get(region.lower(), {})

        accounts = cls.get_accounts_by_region(region_portfolios, region)

        open_orders = order_region[region]
        order_status_res = ListOrders.pipe_to_list(list_client_orders.order_status)

        query = open_orders.build_query(
            accounts=accounts,
            offset=list_client_orders.offset,
            limit=list_client_orders.limit,
            order_status=order_status_res,
        )
        user_open_orders = open_orders.oracle_singleton_instance.get_data(sql=query)
        data = [
            await ListOrders.normalize_open_order(user_open_order, list_client_orders.region)
            for user_open_order in user_open_orders
        ]
        return data
