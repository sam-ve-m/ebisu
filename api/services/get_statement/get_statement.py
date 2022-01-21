from heimdall_client.bifrost import Heimdall
import logging
from api.core.interfaces.interface import IService
from fastapi import Request, Response
from api.domain.enums.region import Region
from api.utils.statement.utils import Statement

log = logging.getLogger()


class GetStatement(IService):
    oracle_singleton_instance = None

    def __init__(
            self,
            request: Request,
            region: Region,
            limit: int,
            offset: float,
            start_date: float,
            end_date: float
    ):
        self.region = region.value
        self.jwt = request.headers.get("x-thebs-answer")
        self.bovespa_account = None
        self.bmf_account = None
        self.limit = limit
        self.offset = offset
        self.start_date = start_date
        self.end_date = end_date

    def get_account(self):
        heimdall = Heimdall(logger=log)
        jwt_data = heimdall.decrypt_payload(jwt=self.jwt)
        self.bovespa_account = jwt_data.get("bovespa_account")
        self.bmf_account = jwt_data.get("bmf_account")

    async def get_service_response(self) -> dict:
        self.get_account()
        if self.region == 'US':
            us_statement = await Statement.get_dw_statement(self.start_date, self.end_date, self.limit)
            return us_statement
        start_date = Statement.from_timestamp_to_utc_isoformat_br(self.offset)
        end_date = Statement.from_timestamp_to_utc_isoformat_br(self.end_date)
        query = f"""SELECT DT_LANCAMENTO, DS_LANCAMENTO, VL_LANCAMENTO 
                   FROM CORRWIN.TCCMOVTO 
                   WHERE CD_CLIENTE = {self.bmf_account} 
                   AND DT_LANCAMENTO >= TO_DATE('{start_date}', 'yyyy-MM-dd')
                   AND DT_LANCAMENTO <= TO_DATE('{end_date}', 'yyyy-MM-dd')
                   ORDER BY NR_LANCAMENTO
                   fetch first {self.limit}  row only
                   """
        statement = GetStatement.oracle_singleton_instance.get_data(sql=query)
        query = f"SELECT VL_TOTAL FROM CORRWIN.TCCSALDO WHERE CD_CLIENTE = {self.bmf_account}"
        balance = GetStatement.oracle_singleton_instance.get_data(sql=query)

        return {
                'balance': balance.pop().get("VL_TOTAL"),
                'statement': [Statement.normalize_statement(transc) for transc in statement]
                }

