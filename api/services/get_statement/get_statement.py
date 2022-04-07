import logging

from api.services.jwt.service import jwt_validator_and_decompile
from api.core.interfaces.interface import IService
from fastapi import Depends
from api.domain.enums.region import Region

from api.repositories.statements.repository import StatementsRepository
from api.services.statement.service import Statement


log = logging.getLogger()


class GetStatement(IService):
    oracle_singleton_instance = StatementsRepository

    def __init__(
        self,
        region: Region,
        limit: int,
        offset: int,
        start_date: float,
        end_date: float,
        decompiled_jwt: dict = Depends(jwt_validator_and_decompile),
    ):
        self.dw_account = None
        self.region = region.value
        self.jwt = decompiled_jwt
        self.bovespa_account = None
        self.bmf_account = None
        self.limit = limit
        self.offset = offset
        self.start_date = start_date
        self.end_date = end_date

    def get_account(self):
        user = self.jwt.get("user", {})
        portfolios = user.get("portfolios", {})
        br_portfolios = portfolios.get("br", {})
        us_portfolios = portfolios.get("us", {})
        self.dw_account = us_portfolios.get("dw_account")
        self.bovespa_account = br_portfolios.get("bovespa_account")
        self.bmf_account = br_portfolios.get("bmf_account")

    async def get_service_response(self) -> dict:
        self.get_account()
        if self.region == "US":
            us_statement = await Statement.get_dw_statement(
                self.dw_account, self.start_date, self.offset, self.end_date, self.limit
            )
            return us_statement
        start_date = Statement.from_timestamp_to_utc_isoformat_br(self.start_date)
        end_date = Statement.from_timestamp_to_utc_isoformat_br(self.end_date)
        query = f"""SELECT DT_LANCAMENTO, DS_LANCAMENTO, VL_LANCAMENTO 
                   FROM CORRWIN.TCCMOVTO 
                   WHERE CD_CLIENTE = {self.bmf_account} 
                   AND DT_LANCAMENTO >= TO_DATE('{start_date}', 'yyyy-MM-dd')
                   AND DT_LANCAMENTO <= TO_DATE('{end_date}', 'yyyy-MM-dd')                   
                   ORDER BY NR_LANCAMENTO
                   OFFSET {self.offset} rows
                   fetch first {self.limit} row only
                   """
        statement = GetStatement.oracle_singleton_instance.get_data(sql=query)
        query = f"SELECT VL_TOTAL FROM CORRWIN.TCCSALDO WHERE CD_CLIENTE = {self.bmf_account}"
        balance = GetStatement.oracle_singleton_instance.get_data(sql=query)

        data_balance = {
            "balance": balance.pop().get("VL_TOTAL"),
            "statements": [
                Statement.normalize_statement(transc) for transc in statement
            ],
        }
        if not data_balance:
            return {}
        return data_balance
