from src.domain.abstract_classes.services.funding_and_withdrawal.money_flow_resolvers.abstract_class import (
    MoneyFlowResolverAbstract,
)
from datetime import datetime, timedelta

from src.domain.exception.model import MoneyFlowPerformedOutsideTransactionWindow
from src.repositories.funding_and_withdrawal.realtime.repository import (
    RealtimeFundingAndWithdrawalRepository,
)
from src.infrastructures.env_config import config


class TransferToExternalBank(MoneyFlowResolverAbstract):
    @staticmethod
    def _get_period():
        # open transfer window
        window_open_at = config("TRANSFER_WINDOW_START").replace(":", "")
        window_close_at = config("TRANSFER_WINDOW_END").replace(":", "")
        return int(window_open_at), int(window_close_at)

    @staticmethod
    def _time_windows_is_open() -> bool:
        window_open_at, window_close_at = TransferToExternalBank._get_period()
        current_hour_and_minute = TransferToExternalBank._get_current_local_time()
        is_open = window_open_at < current_hour_and_minute < window_close_at
        return is_open

    @staticmethod
    def _get_current_local_time() -> int:
        hour_and_minute = datetime.utcnow().strftime("%H%M%S")
        return int(hour_and_minute)

    @staticmethod
    def _is_weekend():
        week_day = datetime.utcnow().weekday()
        return week_day in [5, 6]

    async def _apply_rule(self):
        is_weekend = self._is_weekend()
        time_windows_is_open = self._time_windows_is_open()
        if is_weekend or not time_windows_is_open:
            raise MoneyFlowPerformedOutsideTransactionWindow()

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
