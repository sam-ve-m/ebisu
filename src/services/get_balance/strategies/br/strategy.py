from src.repositories.statements.repository import StatementsRepository
from typing import List

class GetBrBalance:

    oracle_singleton_instance = StatementsRepository

    @staticmethod
    async def get_balance(account: str) -> str:
        query = f"""SELECT VL_TOTAL FROM CORRWIN.TCCSALDO WHERE CD_CLIENTE = {account}"""
        balance = GetBrBalance.oracle_singleton_instance.get_data(sql=query)

        if not balance:
            return {}
        balance_response = {"balance": balance.pop().get("VL_TOTAL")}
        return balance_response
