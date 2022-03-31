from abc import ABC, abstractmethod


class IBankTransfer(ABC):

    @staticmethod
    async def get_bank_transfer_account():
        pass
