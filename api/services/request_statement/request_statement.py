from datetime import datetime, timedelta

from heimdall_client.bifrost import Heimdall
import logging
from api.core.interfaces.interface import IService
from fastapi import Request, Response
from api.domain.enums.region import Region
from api.utils.statement.utils import Statement
import pdfkit
import json
import time
log = logging.getLogger()


class RequestStatement(IService):
    oracle_singleton_instance = None
    s3_singleton = None

    def __init__(
            self,
            request: Request,
            region: Region,
    ):
        self.region = region.value
        self.jwt = request.headers.get("x-thebs-answer")
        self.bovespa_account = None
        self.bmf_account = None
        self.cpf = None
        self.start_date = (datetime.now() - timedelta(days=90)).timestamp() * 1000
        self.end_date = time.time() * 1000

    def get_account(self):
        heimdall = Heimdall(logger=log)
        jwt_data = heimdall.decrypt_payload(jwt=self.jwt)
        self.bovespa_account = jwt_data.get("bovespa_account")
        self.bmf_account = jwt_data.get("bmf_account")
        self.cpf = jwt_data.get("email")

    async def get_service_response(self) -> dict:
        self.get_account()
        if self.region == 'US':
            us_statement = await Statement.get_dw_statement(self.start_date, self.end_date)
            return us_statement
        start_date = Statement.from_timestamp_to_utc_isoformat_br(self.start_date)
        end_date = Statement.from_timestamp_to_utc_isoformat_br(self.end_date)
        query = f"""SELECT DT_LANCAMENTO, DS_LANCAMENTO, VL_LANCAMENTO 
                   FROM CORRWIN.TCCMOVTO 
                   WHERE CD_CLIENTE = {self.bmf_account} 
                   AND DT_LANCAMENTO > TO_DATE('{start_date}', 'yyyy-MM-dd')
                   AND DT_LANCAMENTO <= TO_DATE('{end_date}', 'yyyy-MM-dd')
                   ORDER BY DT_LANCAMENTO
                   """
        statement = RequestStatement.oracle_singleton_instance.get_data(sql=query)
        pdf = pdfkit.from_string(json.dumps({
                'Extrato': [Statement.normalize_statement(transc) for transc in statement]
                }))
        file_duration = (datetime.now() - timedelta(minutes=1)).isoformat()

        RequestStatement.s3_singleton.upload_file(file_path=self.generate_path(), content=pdf, expire_date=file_duration)
        result = RequestStatement.s3_singleton.generate_file_link(file_path=self.generate_path())
        return result

    def generate_path(self):
        path = f"{self.cpf}/statements/{self.start_date}-{self.end_date}.pdf"
        return path