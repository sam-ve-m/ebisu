from abc import abstractmethod
from datetime import datetime
from typing import Tuple

from src.core.interfaces.domain.models.internal.account_transfer.interface import (
    IAccountTransfer,
)
from src.domain.enums.currency import Currency
from src.core.interfaces.services.funding_and_withdrawal.money_flow_resolvers.interface import (
    IBaseMoneyFlowResolver,
)
from src.repositories.funding_and_withdrawal.queue.repository import (
    FundingAndWithdrawalRepository,
)
from src.exceptions.exceptions import UnableToProcessMoneyFlow


class MoneyFlowResolverAbstract(IBaseMoneyFlowResolver):
    def __init__(
        self,
        origin_account: IAccountTransfer,
        account_destination: IAccountTransfer,
        value: float,
    ):
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

    async def _send(
        self,
        resume: dict,
        funding_and_withdrawal_repository=FundingAndWithdrawalRepository,
    ):
        topic = self._get_topic_name()
        was_sent = await funding_and_withdrawal_repository.send_to_bifrost(
            topic=topic, message=resume
        )
        if not was_sent:
            raise UnableToProcessMoneyFlow()

    async def _build_resume(self) -> dict:
        cash_conversion = ">".join([currency.value for currency in self._cash_conversion])
        resume = {
            "origin_account": await self._origin_account.resume(),
            "account_destination": await self._account_destination.resume(),
            "cash_conversion": cash_conversion,
            "value": self._value,
            "tax": self._tax,
            "spread": self._spread,
            "convert_value": self._converted_value,
            "due_date": self._due_date,
        }
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
