from src.services.statement.service import Statement


class GetUsBalance:
    @staticmethod
    async def get_balance(account: str) -> str:
        balance_us = await Statement.get_dw_balance(account)
        return balance_us
