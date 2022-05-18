from src.domain.enums.region import Region
from src.domain.exception.model import InvalidAccountsOwnership
from src.domain.currency_map.country_to_currency.map import country_to_currency
from src.domain.exception.model import NotMappedCurrency
from src.domain.enums.currency import Currency


class AccountTransfer:

    def __init__(
        self,
        account_number: str,
        country: Region,
        user_portfolios: dict
    ):
        self._account_number = account_number
        self._country = country
        self._user_portfolios = user_portfolios
        self._default_accounts =  list()
        self._vnc_accounts =  list()
        self._extract_accounts()
        self._currency = self._get_currency_by_country()
        self.__is_owned_by_user = None
        self.__is_primary_account = None

    def _extract_accounts(self):
        country = self._country.value.lower()
        for accounts_classification, accounts_by_region in self._user_portfolios.items():
            if accounts_representation := accounts_by_region.get(country):
                if accounts_classification == "default":
                    self._default_accounts += accounts_representation.values()
                elif accounts_classification == "vnc":
                    for account_struct in accounts_representation:
                        self._vnc_accounts += account_struct.values()

    def validate_accounts_ownership(self):
        if self._account_number not in self._default_accounts + self._vnc_accounts:
            raise InvalidAccountsOwnership()
        self.__is_owned_by_user = True
        return self

    def validate_that_is_primary_account(self):
        self.__is_primary_account = self._account_number in self._default_accounts
        return self

    def get_fingerprint(self):
        return self._country, self.__is_primary_account

    def _get_currency_by_country(self) -> Currency:
        currency = country_to_currency.get(self._country)
        if not currency:
            raise NotMappedCurrency()
        return currency

    def get_currency(self) -> Currency:
        return self._currency

    def resume(self):
        return {
            "account_number": self._account_number,
            "country": self._country,
            "currency":  self._currency
        }