from etria_logger import Gladsheim

from src.domain.enums.region import Region
from src.domain.validators.exchange_info.get_balance_validator import GetBalanceModel
from src.domain.validators.exchange_info.get_closure_steps_validator import (
    ClosureStepsModel,
)
from src.domain.validators.exchange_info.get_earnings_client import EarningsClientModel
from src.repositories.user_portfolios.repository import UserPortfoliosRepository
from src.services.earnings_from_client.get_earnings_from_client import (
    EarningsFromClient,
)
from src.services.get_balance.service import BalanceService
from src.services.user_positions.service import UserPositionsService


class ClosureSteps:
    balance_service = BalanceService
    earnings_service = EarningsFromClient
    positions_service = UserPositionsService

    account_type_by_region = {"BR": "bmf_account", "US": "dw_account"}

    @staticmethod
    def __get_unique_id_from_jwt_data(jwt_data: dict) -> str:
        unique_id = jwt_data["user"]["unique_id"]
        return unique_id

    @classmethod
    async def _verify_balance(cls, region: str, jwt_data: dict) -> bool:
        balance_model = GetBalanceModel(region=region)
        try:
            balance = await cls.balance_service.get_service_response(
                balance=balance_model, jwt_data=jwt_data
            )
            has_no_balance = not balance.has_balance()
            return has_no_balance
        except Exception as ex:
            message = "Failed to verify balance"
            Gladsheim.error(error=ex, message=message, region=region)
            raise ex

    @classmethod
    async def _verify_positions(cls, region: str, jwt_data: dict) -> bool:
        try:
            positions = await cls.positions_service.get_positions_by_region(
                region=region,
                jwt_data=jwt_data
            )

            has_no_positions = not positions
            return has_no_positions

        except Exception as ex:
            message = "Failed to verify positions"
            Gladsheim.error(error=ex, message=message, region=region)
            raise ex

    @classmethod
    async def _verify_earnings(cls, region: str, jwt_data: dict) -> bool:
        earnings_model = EarningsClientModel(region=region, limit=1)
        try:
            earnings_service_response = await cls.earnings_service.get_service_response(
                earnings_client=earnings_model, jwt_data=jwt_data
            )
            payable_earnings = bool(earnings_service_response.payable)
            record_date_earnings = bool(earnings_service_response.record_date)

            earnings = payable_earnings or record_date_earnings
            has_no_earnings = not earnings
            return has_no_earnings

        except Exception as ex:
            message = "Failed to verify earnings"
            Gladsheim.error(error=ex, message=message, region=region)
            raise ex

    @classmethod
    async def get_closure_steps_by_region(cls, region: str, jwt_data: dict) -> tuple:
        result = {
            "balance": await cls._verify_balance(region, jwt_data),
            "positions": await cls._verify_positions(region, jwt_data),
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
