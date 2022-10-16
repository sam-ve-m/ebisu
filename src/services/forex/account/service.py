# Ebisu
from src.domain.exceptions.repository.forex.exception import (
    ErrorTryingToGetForexAccountData,
    ErrorTryingToGetForexClientId,
    ErrorTryingToGetForexAccountNumber,
)
from src.domain.exceptions.service.forex.exception import ErrorTryingToGetUniqueId
from src.repositories.user.repository import UserRepository

# Standards
from typing import Union


class ForexAccount:
    @classmethod
    async def get_client_id(
        cls, jwt_data: dict
    ) -> Union[int, ErrorTryingToGetForexClientId]:
        unique_id = await cls.__get_unique_id(jwt_data=jwt_data)
        forex_account_data = await cls.__get_forex_account_data(unique_id=unique_id)
        forex_client_id = (
            forex_account_data.get("ouro_invest", {})
            .get("account", {})
            .get("client_id")
        )
        if not forex_client_id:
            raise ErrorTryingToGetForexClientId()
        return int(forex_client_id)

    @classmethod
    async def get_account_number(
        cls, jwt_data: dict
    ) -> Union[int, ErrorTryingToGetForexAccountNumber]:
        unique_id = await cls.__get_unique_id(jwt_data=jwt_data)
        forex_account_data = await cls.__get_forex_account_data(unique_id=unique_id)
        forex_account_number = (
            forex_account_data.get("ouro_invest", {})
            .get("account", {})
            .get("account_number")
        )
        if not forex_account_number:
            raise ErrorTryingToGetForexAccountNumber()
        return int(forex_account_number)

    @classmethod
    async def __get_forex_account_data(
        cls, unique_id
    ) -> Union[dict, ErrorTryingToGetForexAccountData]:
        forex_account_data = await UserRepository.get_forex_account_data(
            unique_id=unique_id
        )
        if not forex_account_data:
            raise ErrorTryingToGetForexAccountData()
        return forex_account_data

    @staticmethod
    async def __get_unique_id(jwt_data: dict) -> Union[str, ErrorTryingToGetUniqueId]:
        unique_id = jwt_data.get("user", {}).get("unique_id")
        if not unique_id:
            raise ErrorTryingToGetUniqueId()
        return unique_id
