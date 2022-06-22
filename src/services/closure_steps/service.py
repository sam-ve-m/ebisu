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
from src.services.get_balance.service import GetBalance
from src.services.user_positions.service import UserPositionsService


class ClosureSteps:
    balance_service = GetBalance
    earnings_service = EarningsFromClient
    positions_service = UserPositionsService

    account_type_by_region = {"BR": "bmf_account", "US": "dw_account"}

    @staticmethod
    def __get_unique_id_from_jwt_data(jwt_data: dict) -> str:
        unique_id = jwt_data["user"]["unique_id"]
        return unique_id

    @classmethod
    async def _get_user_accounts(cls, region: str, jwt_data: dict) -> list:
        accounts = []
        portfolios: dict = await UserPortfoliosRepository.get_portfolios_by_region(
            unique_id=cls.__get_unique_id_from_jwt_data(jwt_data), region=region
        )

        for key in portfolios:
            if key == "default":
                account_number = portfolios[key][region.lower()][
                    cls.account_type_by_region[region]
                ]
                accounts.append(account_number)
            elif key == "vnc" and portfolios[key].get(region.lower()):
                for account in portfolios[key][region.lower()]:
                    account_number = account[cls.account_type_by_region[region]]
                    accounts.append(account_number)

        return accounts

    @classmethod
    async def _verify_balance(cls, region: str, jwt_data: dict) -> bool:
        balance_model = GetBalanceModel(region=region)
        balance_service_response = await cls.balance_service.get_service_response(
            balance=balance_model, jwt_data=jwt_data
        )
        balance = balance_service_response.get("balance")
        balance = int(balance) if balance is not None else 0

        if balance != 0:
            return False
        return True

    @classmethod
    async def _verify_positions(cls, region: str, jwt_data: dict) -> bool:
        accounts = await cls._get_user_accounts(region, jwt_data)
        positions = await cls.positions_service.get_positions_by_region(
            region, accounts
        )
        if positions != 0:
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
            "positions": await cls._verify_positions(region, jwt_data),
            "earnings": await cls._verify_earnings(region, jwt_data)
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
