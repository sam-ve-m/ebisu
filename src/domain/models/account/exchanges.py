from src.core.interfaces.domain.models.internal.account_transfer.interface import (
    IAccountTransfer,
)
from src.domain.models.account.fingerprit import Fingerprint, IsPrimaryAccount
from src.domain.enums.region import Region
from src.domain.exceptions.model import InvalidAccountsOwnership
from src.domain.currency_map.country_to_currency.map import country_to_currency
from src.domain.exceptions.model import NotMappedCurrency
from src.domain.enums.currency import Currency
from src.repositories.user.repository import UserRepository
from src.repositories.user_exchange.repository import UserExchangeRepository


class ExchangeAccount(IAccountTransfer):
    def __init__(self, account_number: str, country: Region, user_unique_id: str):
        self._account_number = account_number
        self._country = country
        self._user_unique_id = user_unique_id
        self._default_accounts = list()
        self._vnc_accounts = list()
        self._currency = self._get_currency_by_country()
        self.__is_owned_by_user = None
        self.__is_primary_account = None

    async def _extract_accounts(self):
        country = self._country.value.lower()
        user_portfolios = await UserRepository.get_user_portfolios(
            unique_id=self._user_unique_id
        )

        def filter_accounts_representation(values):
            results = list(filter(lambda x: isinstance(x, str), values))
            return results

        for (
            accounts_classification,
            accounts_by_region,
        ) in user_portfolios.items():
            if accounts_representation := accounts_by_region.get(country):
                if accounts_classification == "default":
                    self._default_accounts += filter_accounts_representation(
                        accounts_representation.values()
                    )
                elif accounts_classification == "vnc":
                    for account_struct in accounts_representation:
                        self._vnc_accounts += filter_accounts_representation(
                            account_struct.values()
                        )

    async def validate_accounts_ownership(self):
        await self._extract_accounts()
        self.__is_primary_account = self._validate_that_is_primary_account()

        if self._account_number not in self._default_accounts + self._vnc_accounts:
            raise InvalidAccountsOwnership()
        self.__is_owned_by_user = True
        return self

    def get_fingerprint(self) -> Fingerprint:
        fingerprint = (self._country, self.__is_primary_account)
        return fingerprint

    def _validate_that_is_primary_account(self) -> IsPrimaryAccount:
        is_primary_account = IsPrimaryAccount(
            self._account_number in self._default_accounts
        )
        return is_primary_account

    def _get_currency_by_country(self) -> Currency:
        currency = country_to_currency.get(self._country)
        if not currency:
            raise NotMappedCurrency()
        return currency

    def get_currency(self):
        return self._currency

    async def resume(self):
        return {
            "user_unique_id": self._user_unique_id,
            "account_number": self._account_number,
            "country": self._country,
            "currency": self._currency,
        }
