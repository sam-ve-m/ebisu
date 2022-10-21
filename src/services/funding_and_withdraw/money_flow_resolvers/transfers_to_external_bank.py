from datetime import datetime

from src.core.interfaces.domain.models.internal.account_transfer.interface import (
    IAccountTransfer,
)
from src.domain.exceptions.service.funding_and_withdraw.money_flow_resolvers.model import \
    MoneyFlowPerformedOutsideTransactionWindow

from src.infrastructures.env_config import config
from src.transport.bank_transfer.bifrost.transport import BankTransferBifrostTransport


class TransferToExternalBank:
    def __init__(
        self,
        origin_account: IAccountTransfer,
        account_destination: IAccountTransfer,
        value: float,
    ):
        self._origin_account = origin_account
        self._account_destination = account_destination
        self._value = value

    @staticmethod
    def _get_period():
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

    @staticmethod
    async def _send(resume: dict):
        await BankTransferBifrostTransport.send_transfer_message_to_bifrost(
            message=resume
        )

    async def _build_resume(self) -> dict:
        resume = {
            "origin_account": await self._origin_account.resume(),
            "account_destination": await self._account_destination.resume(),
            "value": self._value,
            "due_date": datetime.utcnow(),
        }
        return resume

    async def __call__(self, *args, **kwargs) -> dict:
        await self._apply_rule()
        resume = await self._build_resume()
        await self._send(resume=resume)
        return resume
