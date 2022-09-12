# Internal Lib
from typing import List

from src.domain.enums.order_status import OrderStatus
from src.domain.enums.region import Region
from src.domain.validators.exchange_info.list_client_order_validator import (
    ListClientOrderModel,
)
from src.repositories.companies_data.repository import CompanyInformationRepository
from src.services.list_client_orders.strategies import order_region
from src.domain.time_formatter.time_formatter import str_to_timestamp
from src.domain.currency_map.country_to_currency.map import country_to_currency


class ListOrders:
    company_information_repository = CompanyInformationRepository

    @classmethod
    def pipe_to_list(cls, data: str):
        list_data = None
        if isinstance(data, str):
            data = data.upper()
            list_data = data.split("|")

        if list_data is None:
            return []

        return [OrderStatus[status] for status in list_data]

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
        side = user_trade.get("SIDE")
        normalized_data = {
            "name": await ListOrders.company_information_repository.get_company_name(
                user_trade.get("SYMBOL")
            ),
            "cl_order_id": user_trade.get("CLORDID"),
            "root_cl_order_id": user_trade.get("ROOTCLORDID"),
            "time": str_to_timestamp(user_trade.get("CREATEDAT")),
            "quantity": user_trade.get("ORDERQTY"),
            "order_type": user_trade.get("ORDTYPE"),
            "average_price": ListOrders.decimal_128_converter(user_trade, "AVGPX"),
            "currency": currency.value,
            "symbol": user_trade.get("SYMBOL"),
            "status": user_trade.get("ORDSTATUS"),
            "price": user_trade.get("PRICE"),
            "stop": user_trade.get("STOPPX"),
            "side": side.lower() if side else side,
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
        cls, jwt_data: dict, list_client_orders: ListClientOrderModel
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
            await ListOrders.normalize_open_order(
                user_open_order, list_client_orders.region
            )
            for user_open_order in user_open_orders
        ]
        return data
