class GetUsBalance:
    dw = DWTransport()

    @classmethod
    async def get_balance(cls, account: str) -> str:
        balance_us = await cls.get_dw_balance(account)
        return balance_us

    @staticmethod
    async def get_dw_balance(dw_account: str):
        raw_balance = await Statement.dw.get_balances(dw_account)
        balance = Statement.normalize_balance_us(*raw_balance)
        return {"balance": balance}