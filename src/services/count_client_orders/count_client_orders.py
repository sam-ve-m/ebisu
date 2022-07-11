# Internal Lib
from typing import List

from src.domain.enums.order_status import OrderStatus
from src.domain.enums.region import Region
from src.domain.validators.exchange_info.count_client_order_validator import (
    GetClientOrderQuantityModel,
)
from src.repositories.companies_data.repository import CompanyInformationRepository
from src.services.count_client_orders.strategies import order_region


class CountOrders:
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
        cls, jwt_data: dict, client_order_quantity: GetClientOrderQuantityModel
    ) -> List[dict]:
        user = jwt_data.get("user", {})
        portfolios = user.get("portfolios", {})

        region = client_order_quantity.region.value
        region_portfolios = portfolios.get(region.lower(), {})

        accounts = cls.get_accounts_by_region(region_portfolios, region)

        open_orders = order_region[region]
        order_status_res = CountOrders.pipe_to_list(client_order_quantity.order_status)

        query = open_orders.build_query(
            accounts=accounts,
            order_status=order_status_res,
        )
        orders_in_status = open_orders.oracle_singleton_instance.get_data(sql=query)
        if orders_in_status:
            count = orders_in_status.pop()
            data = {"quantity": count["COUNT"]}
            return data
