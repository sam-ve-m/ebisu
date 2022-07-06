from src.repositories.statements.repository import StatementsRepository


class GetBrBalance:

    oracle_singleton_instance = StatementsRepository

    @staticmethod
    async def get_balance(account: str) -> dict:
        query = (
            f"""SELECT VL_TOTAL FROM CORRWIN.TCCSALDO WHERE CD_CLIENTE = {account}"""
        )
        balance = GetBrBalance.oracle_singleton_instance.get_data(sql=query)

        if not balance:
            return {"balance": -1}
        balance_response = {"balance": balance.pop().get("VL_TOTAL")}
        return balance_response
