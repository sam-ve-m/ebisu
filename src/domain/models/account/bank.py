from src.core.interfaces.domain.models.internal.account_transfer.interface import (
    IAccountTransfer,
)
from src.domain.models.account.fingerprit import Fingerprint, IsPrimaryAccount
from src.repositories.bank_account.repository import UserBankAccountRepository
from src.domain.enums.region import Region
from src.domain.exception.model import InvalidAccountsOwnership
from src.domain.currency_map.country_to_currency.map import country_to_currency
from src.domain.exception.model import NotMappedCurrency
from src.domain.enums.currency import Currency


class BankAccount(IAccountTransfer):
    def __init__(self, bank_account_id: str, country: Region, user_unique_id: str):
        self._user_unique_id = user_unique_id
        self._bank_account_id = bank_account_id
        self._country = country
        self._currency = self._get_currency_by_country()
        self.__is_owned_by_user = None
        self.__is_primary_account = IsPrimaryAccount(False)

    async def validate_accounts_ownership(self):
        self.__is_primary_account = self._validate_that_is_primary_account()
        is_bank_account_from_user = (
            await UserBankAccountRepository.user_bank_account_id_exists(
                unique_id=self._user_unique_id, bank_account_id=self._bank_account_id
            )
        )
        if not is_bank_account_from_user:
            raise InvalidAccountsOwnership()
        return self

    @staticmethod
    def _validate_that_is_primary_account() -> IsPrimaryAccount:
        return IsPrimaryAccount(False)

    def get_fingerprint(self) -> Fingerprint:
        fingerprint = (self._country, self.__is_primary_account)
        return fingerprint

    def _get_currency_by_country(self) -> Currency:
        currency = country_to_currency.get(self._country)
        if not currency:
            raise NotMappedCurrency()
        return currency

    def get_currency(self):
        return self._currency

    async def resume(self):
        account_details = await UserBankAccountRepository.get_user_bank_account_by_id(
            unique_id=self._user_unique_id, bank_account_id=self._bank_account_id
        )
        return {
            "account_details": account_details,
            "account_number": self._bank_account_id,
            "country": self._country,
            "currency": self._currency,
        }
