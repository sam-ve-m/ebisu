from etria_logger import Gladsheim

from src.repositories.statements.repository import StatementsRepository


class GetBrBalance:

    oracle_singleton_instance = StatementsRepository

    @staticmethod
    async def get_balance(account: str) -> dict:
        query = (
            f"""SELECT VL_TOTAL FROM CORRWIN.TCCSALDO WHERE CD_CLIENTE = {account}"""
        )
        try:
            balance = GetBrBalance.oracle_singleton_instance.get_data(sql=query)
            balance_value = balance.pop()["VL_TOTAL"]
            if balance_value is None:
                balance_value = 0
            balance_value = float(balance_value)

        except Exception as ex:
            Gladsheim.error(
                message=f"GetBrBalance::get_balance::Error to get balance in BR",
                account=account,
                error=ex,
            )
            raise ex

        balance_response = {"balance": balance_value}
        return balance_response
