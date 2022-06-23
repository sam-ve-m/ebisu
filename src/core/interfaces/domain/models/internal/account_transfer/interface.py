from abc import ABC, abstractmethod

from src.domain.enums.currency import Currency
from src.domain.models.account import Fingerprint


class IAccountTransfer(ABC):

    @abstractmethod
    async def validate_accounts_ownership(self):
        """This method must raise a InvalidAccountsOwnership in case of error"""

    @abstractmethod
    async def resume(self):
        """This method must return the resume of operation request"""

    @abstractmethod
    def get_currency(self) -> Currency:
        """This method must return the currency"""

    @abstractmethod
    def get_fingerprint(self) -> Fingerprint:
        """Return the finger the account fingerprint"""
