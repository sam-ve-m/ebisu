from abc import abstractmethod
from datetime import datetime
from typing import Tuple
from api.domain.enums.currency import Currency
from api.core.interfaces.services.funding_and_withdrawal.money_flow_resolvers.interface import IBaseMoneyFlowResolver
from api.domain.model.internal.account_transfer.model import AccountTransfer
from api.repositories.funding_and_withdrawal.queue.repository import FundingAndWithdrawalRepository
from api.exceptions.exceptions import UnableToProcessMoneyFlow

class MoneyFlowResolverAbstract(IBaseMoneyFlowResolver):

    def __init__(self, origin_account: AccountTransfer, account_destination: AccountTransfer, value: float):
        self._origin_account = origin_account
        self._account_destination = account_destination
        self._cash_conversion = self._get_cash_conversion_references()
        self._value = value
        self._tax = None
        self._spread = None
        self._converted_value = None
        self._due_date = None

    def _get_cash_conversion_references(self) -> Tuple[Currency, Currency]:
        origin_account_currency = self._origin_account.get_currency()
        account_destination_currency = self._account_destination.get_currency()
        return origin_account_currency, account_destination_currency

    async def _get_base_value(self) -> float:
        return self._value

    @abstractmethod
    async def _get_spread(self) -> float:
        pass

    @abstractmethod
    async def _get_tax(self) -> float:
        pass

    @abstractmethod
    async def _convert_value(self) -> float:
        pass

    @abstractmethod
    async def _calculate_due_date(self) -> datetime:
        pass

    @abstractmethod
    def _get_topic_name(self) -> str:
        pass

    async def _send(self, resume: dict, funding_and_withdrawal_repository=FundingAndWithdrawalRepository):
        topic = self._get_topic_name()
        was_sent = await funding_and_withdrawal_repository.send_to_bifrost(topic=topic, message=resume)
        if not was_sent:
            raise UnableToProcessMoneyFlow()

    async def _build_resume(self) -> dict:
        details = {
            "tax": self._tax,
            "spread": self._spread,
            "convert_value": self._converted_value,
            "due_date": self._due_date,
        }
        origin_account_currency, account_destination_currency = self._get_cash_conversion_references()
        resume = {
            "origin_account": self._origin_account.resume(),
            "account_destination": self._account_destination.resume(),
            "value": self._value,
            "cash_conversion": f"{origin_account_currency.value} > {account_destination_currency.value}",
        }
        for detail, value in details.items():
            if value:
                resume.update({detail: value})
        return resume


    async def __call__(self, *args, **kwargs) -> dict:
        self._spread = await self._get_spread()
        self._tax = await self._get_tax()
        self._converted_value = await self._convert_value()
        self._due_date = await self._calculate_due_date()
        resume = await self._build_resume()
        # TO PERSEPHONE
        await self._send(resume=resume)
        return resume
