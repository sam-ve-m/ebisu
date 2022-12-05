# Ebisu
from src.domain.exceptions.repository.forex.model import (
    ErrorTryingToGetForexClientId,
    ErrorTryingToGetForexAccountNumber,
    ErrorTryingToGetForexAccountData,
)
from src.repositories.user.repository import UserRepository

# Standards
from typing import Union


class ForexAccount:
    @classmethod
    async def get_client_id(
        cls, unique_id: str
    ) -> Union[int, ErrorTryingToGetForexClientId]:
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
        cls, unique_id: str
    ) -> Union[int, ErrorTryingToGetForexAccountNumber]:
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
        cls, unique_id: str
    ) -> Union[dict, ErrorTryingToGetForexAccountData]:
        forex_account_data = await UserRepository.get_forex_account_data(
            unique_id=unique_id
        )
        if not forex_account_data:
            raise ErrorTryingToGetForexAccountData()
        return forex_account_data
