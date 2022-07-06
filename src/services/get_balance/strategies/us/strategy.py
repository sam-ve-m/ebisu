from mepho import DWApiTransport


class GetUsBalance:
    dw = DWApiTransport

    @classmethod
    async def get_dw_balance(cls, dw_account: str):
        raw_balance = await cls.dw.get_balances(dw_account)
        balance = cls.normalize_balance_us(*raw_balance)
        return {"balance": balance}

    @staticmethod
    def normalize_balance_us(client_balance: dict) -> dict:
        balance = client_balance.get("dict_body", {}).get("cash", {}).get("cashBalance", 0)
        return balance