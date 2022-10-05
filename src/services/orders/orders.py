# Internal Lib
from typing import List

from nidavellir import Sindri

from src.domain.enums.order_status import OrderStatus
from src.domain.enums.order_tifs import OrderTifs
from src.domain.enums.region import Region
from src.domain.models.database.client_orders.model import ClientOrdersModel
from src.domain.models.database.client_orders_quantity.model import QuantityModel
from src.domain.models.response.client_orders.response_model import ClientOrdersResponse
from src.domain.models.response.client_orders_quantity.response_model import QuantityResponse
from src.domain.validators.exchange_info.client_orders_validator import GetClientOrderModel
from src.domain.validators.exchange_info.count_client_order_validator import GetClientOrderQuantityModel
from src.domain.validators.exchange_info.list_client_order_validator import (
    ListClientOrderModel,
)
from src.domain.models.database.list_client_orders.model import ClientListOrdersModel
from src.domain.validators.orders.order_status import OrderStatusValidator
from src.repositories.companies_data.repository import CompanyInformationRepository
from src.domain.time_formatter.time_formatter import str_to_timestamp
from src.domain.currency_map.country_to_currency.map import country_to_currency
from src.domain.models.response.list_client_orders.response_model import ClientListOrdersResponse
from src.domain.responses.http_response_model import ResponseModel
from src.domain.enums.response.internal_code import InternalCode
from http import HTTPStatus

from src.services.orders.strategies import order_region


class Orders:
    company_information_repository = CompanyInformationRepository

    @staticmethod
    def decimal_128_converter(user_trade: dict, field: str) -> float:
        value = user_trade.get(field)
        if value:
            return float(value)
        return 0

    @staticmethod
    async def normalize_list_open_order(user_trade: dict, region: Region) -> ClientListOrdersModel:
        currency = country_to_currency[region]
        accumulated_quantity = user_trade.get("CUMQTY")
        side = user_trade.get("SIDE")
        normalized_data = {
            "name": await Orders.company_information_repository.get_company_name(
                user_trade.get("SYMBOL")
            ),
            "cl_order_id": user_trade.get("CLORDID"),
            "root_cl_order_id": user_trade.get("ROOTCLORDID"),
            "time": str_to_timestamp(user_trade.get("CREATEDAT")),
            "quantity": user_trade.get("ORDERQTY"),
            "order_type": user_trade.get("ORDTYPE"),
            "average_price": Orders.decimal_128_converter(user_trade, "AVGPX"),
            "currency": currency.value,
            "symbol": user_trade.get("SYMBOL"),
            "status": user_trade.get("ORDSTATUS"),
            "price": user_trade.get("PRICE"),
            "stop": user_trade.get("STOPPX"),
            "side": side.lower() if side else side,
            "total_spent": (
                    (accumulated_quantity if accumulated_quantity else float(0.0))
                    * Orders.decimal_128_converter(user_trade, "AVGPX")
            ),
        }
        response_model = ClientListOrdersModel(**normalized_data)

        return response_model

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
    async def get_list_client_orders(
        cls, jwt_data: dict, list_client_orders: ListClientOrderModel
    ) -> ResponseModel:
        user = jwt_data.get("user", {})
        portfolios = user.get("portfolios", {})

        region = list_client_orders.region.value
        region_portfolios = portfolios.get(region.lower(), {})

        accounts = cls.get_accounts_by_region(region_portfolios, region)

        open_orders = order_region[region]

        query = open_orders.build_query(
            accounts=accounts,
            offset=list_client_orders.offset,
            limit=list_client_orders.limit,
            order_status=list_client_orders.order_status,
        )
        user_open_orders = open_orders.oracle_singleton_instance.get_data(sql=query)
        data = [
            await Orders.normalize_list_open_order(user_open_order, list_client_orders.region)
            for user_open_order in user_open_orders
        ]
        response_model = ClientListOrdersResponse.to_response(
            models=data
        )
        return response_model

    @classmethod
    async def get_client_orders_quantity(
            cls, jwt_data: dict, client_order_quantity: GetClientOrderQuantityModel
    ) -> ResponseModel:
        user = jwt_data.get("user", {})
        portfolios = user.get("portfolios", {})

        region = client_order_quantity.region.value
        region_portfolios = portfolios.get(region.lower(), {})

        accounts = cls.get_accounts_by_region(region_portfolios, region)

        open_orders = order_region[region]

        query = open_orders.build_quantity_query(
            accounts=accounts,
            order_status=client_order_quantity.order_status,
        )
        orders_in_status = open_orders.oracle_singleton_instance.get_data(sql=query)
        if orders_in_status:
            count = orders_in_status.pop()
            response_model = QuantityModel(quantity=count["COUNT"])
            quantity_response_model = QuantityResponse.to_response(model=response_model)
            client_quantity_result = quantity_response_model.dict()
            Sindri.dict_to_primitive_types(client_quantity_result)
            return client_quantity_result

    @staticmethod
    def tiff_response_converter(tif_value: str):
        tiff_response = OrderTifs.has_member_value(value=tif_value)
        if tiff_response is not None:
            return tiff_response.value
        return OrderTifs.NOT_AVAILABLE.value

    @staticmethod
    def normalize_client_orders_open_order(user_trade: dict, region: Region) -> ClientOrdersModel:
        side = user_trade.get("SIDE")
        accumulated_quantity = user_trade.get("CUMQTY")
        currency = country_to_currency[region]

        normalized_data = {
            "cl_order_id": user_trade.get("CLORDID"),
            "account": user_trade.get("ACCOUNT"),
            "time": int(str_to_timestamp(user_trade.get("CREATEDAT")) * 1000),
            "quantity": user_trade.get("ORDERQTY"),
            "average_price": Orders.decimal_128_converter(user_trade, "AVGPX"),
            "price": Orders.decimal_128_converter(user_trade, "PRICE"),
            "last_price": Orders.decimal_128_converter(user_trade, "LASTPX"),
            "stop_price": Orders.decimal_128_converter(user_trade, "STOPPX"),
            "currency": currency.value,
            "symbol": user_trade.get("SYMBOL"),
            "side": side.lower() if side else side,
            "status": user_trade.get("ORDSTATUS"),
            "tif": Orders.tiff_response_converter(user_trade.get("TIMEINFORCE")),
            "total_spent": (
                    (accumulated_quantity if accumulated_quantity else float(0.0))
                    * Orders.decimal_128_converter(user_trade, "AVGPX")
            ),
            "quantity_filled": (
                accumulated_quantity if accumulated_quantity else float(0.0)
            ),
            "quantity_leaves": user_trade.get("LEAVESQTY"),
            "quantity_last": user_trade.get("LASTQTY"),
            "text": user_trade.get("TEXT"),
            "reject_reason": user_trade.get("ORDREJREASON"),
            "exec_type": user_trade.get("EXECTYPE"),
            "expire_date": int(str_to_timestamp(user_trade.get("EXPIREDATE")) * 1000)
            if user_trade.get("EXPIREDATE")
            else None,
            "error_message": user_trade.get("MESSAGE"),
        }
        response_model = ClientOrdersModel(**normalized_data)
        return response_model

    @classmethod
    def get_client_orders(
            cls, client_order: GetClientOrderModel, jwt_data: dict
    ) -> ResponseModel:
        user = jwt_data.get("user", {})
        portfolios = user.get("portfolios", {})

        region = client_order.region.value
        region_portfolios = portfolios.get(region.lower(), {})

        accounts = cls.get_accounts_by_region(region_portfolios, region)

        open_orders = order_region[region]
        query = open_orders.build_client_orders_query(
            accounts=accounts, root_cl_order_id=client_order.root_cl_order_id
        )
        user_open_orders = open_orders.oracle_singleton_instance.get_data(sql=query)
        data = [
            Orders.normalize_client_orders_open_order(user_open_order, client_order.region)
            for user_open_order in user_open_orders
        ]
        response_model = ClientOrdersResponse.to_response(
            models=data
        )
        return response_model
