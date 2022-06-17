from src.domain.enums.region import Region
from src.domain.validators.exchange_info.get_balance_validator import GetBalanceModel
from src.domain.validators.exchange_info.get_closure_steps_validator import (
    ClosureStepsModel,
)
from src.domain.validators.exchange_info.get_earnings_client import EarningsClientModel
from src.domain.validators.exchange_info.list_client_order_validator import (
    ListClientOrderModel,
)
from src.services.earnings_from_client.get_earnings_from_client import (
    EarningsFromClient,
)
from src.services.get_balance.service import GetBalance
from src.services.list_client_orders.list_client_orders import ListOrders


class ClosureSteps:
    balance_service = GetBalance
    orders_service = ListOrders
    earnings_service = EarningsFromClient

    @classmethod
    async def _verify_balance(cls, region: str, jwt_data: dict) -> bool:
        balance_model = GetBalanceModel(region=region)
        try:
            balance_service_response = await cls.balance_service.get_service_response(
                balance=balance_model, jwt_data=jwt_data
            )
            balance = int(balance_service_response.get("balance"))
            if balance != 0:
                return False
            return True
        except:
            return True

    @classmethod
    async def _verify_orders(cls, region: str, jwt_data: dict) -> bool:
        orders_model = ListClientOrderModel(
            region=region,
            limit=1,
            offset=0,
            order_status="NEW|PENDING_CANCEL|SUSPENDED|PENDING_NEW|CALCULATED",
        )
        orders_service_response = await cls.orders_service.get_service_response(
            list_client_orders=orders_model, jwt_data=jwt_data
        )
        if orders_service_response != []:
            return False
        return True

    @classmethod
    async def _verify_earnings(cls, region: str, jwt_data: dict) -> bool:
        earnings_model = EarningsClientModel(
            region=region,
            limit=1,
            offset=0,
            earnings_types="DIVIDENDS_AND_OTHER_CASH_INCOME",
        )
        earnings_service_response = cls.earnings_service.get_service_response(
            earnings_client=earnings_model, jwt_data=jwt_data
        )
        earnings = earnings_service_response.get("payable_earnings")
        if earnings != []:
            return False
        return True

    @classmethod
    async def get_closure_steps_by_region(cls, region: str, jwt_data: dict) -> tuple:
        result = {
            "balance": await cls._verify_balance(region, jwt_data),
            "orders": await cls._verify_orders(region, jwt_data),
            "earnings": await cls._verify_earnings(region, jwt_data),
        }
        steps_are_ok = all([value for key, value in result.items()])

        return steps_are_ok, result

    @classmethod
    async def get_service_response(
        cls, closure_steps: ClosureStepsModel, jwt_data: dict
    ) -> dict:
        region = closure_steps.region.value
        status, steps = await cls.get_closure_steps_by_region(region, jwt_data)
        service_response = {"regular": status, "steps_status": {region: steps}}
        if region == Region.BR.value:
            if jwt_data.get("user").get("portfolios").get("us"):
                status_us, steps_us = await cls.get_closure_steps_by_region(
                    Region.US.value, jwt_data
                )
                service_response["steps_status"][Region.US.value] = steps_us
                service_response["regular"] = status and status_us

        return service_response
