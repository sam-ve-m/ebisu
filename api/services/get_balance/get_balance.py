from api.domain.enums.region import Region
from api.repositories.statements.repository import StatementsRepository
from api.services.statement.service import Statement


class GetBalance:
    bmf_account = None
    oracle_singleton_instance = StatementsRepository

    @classmethod
    async def get_service_response(cls, region: Region, jwt_data: dict) -> dict:
        user = jwt_data.get("user", {})
        portfolios = user.get("portfolios", {})
        br_portfolios = portfolios.get("br", {})
        cls.bovespa_account = br_portfolios.get("bovespa_account")
        cls.bmf_account = br_portfolios.get("bmf_account")

        if region == "US":
            balance_us = await Statement.get_dw_balance()
            return balance_us

        query = f"SELECT VL_TOTAL FROM CORRWIN.TCCSALDO WHERE CD_CLIENTE = {cls.bmf_account}"
        balance = GetBalance.oracle_singleton_instance.get_data(sql=query)

        if not balance:
            return {}
        balance_response = {"payload": {
            "balance": balance.pop().get("VL_TOTAL"),
        }}
        return balance_response
