from typing import List

from etria_logger import Gladsheim

from src.domain.account_close_steps.model import AccountCloseSteps
from src.domain.account_close_steps.response.model import AccountCloseStepsToResponse
from src.domain.balance.base.model import BaseBalance
from src.domain.enums.region import Region
from src.domain.exceptions.service.account_close_steps.model import AccountCloseStepsForbidden
from src.domain.positions.model import Position
from src.domain.request.exchange_info.get_balance_validator import GetBalanceModel
from src.domain.request.exchange_info.get_closure_steps_validator import (
    AccountCloseStepsRequest,
)
from src.domain.request.exchange_info.get_earnings_client import EarningsClientModel
from src.services.earnings_from_client.get_earnings_from_client import (
    EarningsFromClient,
)
from src.services.get_balance.service import BalanceService
from src.services.user_positions.service import UserPositionsService


class AccountCloseStepsService:
    balance_service = BalanceService
    earnings_service = EarningsFromClient
    positions_service = UserPositionsService

    account_type_by_region = {"BR": "bmf_account", "US": "dw_account"}

    @staticmethod
    def __get_unique_id_from_jwt_data(jwt_data: dict) -> str:
        unique_id = jwt_data["user"]["unique_id"]
        return unique_id

    @classmethod
    async def __get_balance(cls, region: str, jwt_data: dict) -> BaseBalance:
        balance_model = GetBalanceModel(region=region)
        try:
            balance = await cls.balance_service.get_service_response(
                balance=balance_model, jwt_data=jwt_data
            )

            return balance
        except Exception as ex:
            message = "Failed to get balance"
            Gladsheim.error(error=ex, message=message, region=region)
            raise ex

    @classmethod
    async def __get_positions(cls, region: str, jwt_data: dict) -> List[Position]:
        try:
            positions = await cls.positions_service.get_positions_by_region(
                region=region, jwt_data=jwt_data
            )

            return positions

        except Exception as ex:
            message = "Failed to get positions"
            Gladsheim.error(error=ex, message=message, region=region)
            raise ex

    @classmethod
    async def __get_earnings(cls, region: str, jwt_data: dict) -> any:
        earnings_model = EarningsClientModel(region=region, limit=1)
        try:
            earnings_service_response = await cls.earnings_service.get_service_response(
                earnings_client=earnings_model, jwt_data=jwt_data
            )
            return earnings_service_response

        except Exception as ex:
            message = "Failed to get earnings"
            Gladsheim.error(error=ex, message=message, region=region)
            raise ex

    @classmethod
    async def get_closure_steps_by_region(
        cls, region: str, jwt_data: dict
    ) -> AccountCloseSteps:

        balance = await cls.__get_balance(region, jwt_data)
        positions = await cls.__get_positions(region, jwt_data)
        earnings = await cls.__get_earnings(region, jwt_data)

        account_close_steps = AccountCloseSteps(
            balance=balance, positions=positions, earnings=earnings, region=region
        )

        return account_close_steps

    @classmethod
    async def get_service_response(
        cls, closure_steps: AccountCloseStepsRequest, jwt_data: dict
    ) -> dict:
        region = closure_steps.region.value
        is_br_account = region == Region.BR.value
        is_us_account = region == Region.US.value
        user_portfolios = jwt_data.get("user").get("portfolios", {})
        has_us_account = user_portfolios.get("us", {}).get("dw_account")
        has_br_account = user_portfolios.get("br", {}).get("bmf_account")

        if (is_br_account and not has_br_account) or (
            is_us_account and not has_us_account
        ):
            raise AccountCloseStepsForbidden()

        account_close_steps = await cls.get_closure_steps_by_region(region, jwt_data)
        accounts_close_steps: List[AccountCloseSteps] = []
        accounts_close_steps.append(account_close_steps)

        if is_br_account and has_us_account:
            account_close_steps_us = await cls.get_closure_steps_by_region(
                Region.US.value, jwt_data
            )
            accounts_close_steps.append(account_close_steps_us)

        account_close_steps_response = (
            AccountCloseStepsToResponse.account_close_steps_response(
                accounts_close_steps=accounts_close_steps
            )
        )

        return account_close_steps_response
