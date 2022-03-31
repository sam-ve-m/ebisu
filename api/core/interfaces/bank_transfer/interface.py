from abc import ABC, abstractmethod
from fastapi import Request


class IBankTransfer(ABC):
    @staticmethod
    @abstractmethod
    async def get_bank_transfer_account(request: Request):
        pass
