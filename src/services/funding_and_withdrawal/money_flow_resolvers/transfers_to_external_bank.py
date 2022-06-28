from src.domain.abstract_classes.services.funding_and_withdrawal.money_flow_resolvers.abstract_class import (
    MoneyFlowResolverAbstract,
)
from datetime import datetime, timedelta
from src.repositories.funding_and_withdrawal.realtime.repository import (
    RealtimeFundingAndWithdrawalRepository,
)
from src.infrastructures.env_config import config


class TransferToExternalBank(MoneyFlowResolverAbstract):
    async def _get_spread(self) -> float:
        return 0

    async def _get_tax(self) -> float:
        return 0

    async def _convert_value(self) -> float:
        base_value = await self._get_base_value()
        return base_value

    async def _calculate_due_date(self) -> datetime:
        return datetime.utcnow() + timedelta(days=1)

    def _get_topic_name(self) -> str:
        return config("TRANSFERS_BETWEEN_SINACOR_AND_EXTERNAL_BANK")
