from abc import ABC, abstractmethod
from datetime import datetime
from src.domain.model.internal.account_transfer.model import AccountTransfer
from src.repositories.funding_and_withdrawal.queue.repository import FundingAndWithdrawalRepository


class IBaseMoneyFlowResolver(ABC):

    @abstractmethod
    def __init__(self, origin_account: AccountTransfer, account_destination: AccountTransfer, value: float):
        pass

    @abstractmethod
    async def _get_base_value(self) -> float:
        pass

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
    async def _send(self, resume: dict, funding_and_withdrawal_repository: FundingAndWithdrawalRepository):
        pass

    @abstractmethod
    async def _build_resume(self) -> dict:
        pass

    @abstractmethod
    def _get_topic_name(self) -> str:
        pass
