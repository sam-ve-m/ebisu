import json
import logging
import time
from datetime import datetime, timedelta

import pdfkit
from fastapi import Depends

from api.application_dependencies.jwt_validator import jwt_validator_and_decompile
from api.core.interfaces.interface import IService
from api.domain.enums.region import Region
from api.utils.statement.utils import Statement

log = logging.getLogger()


class RequestStatement(IService):
    oracle_singleton_instance = None
    s3_singleton = None

    def __init__(
            self,
            region: Region,
            decompiled_jwt: dict = Depends(jwt_validator_and_decompile),
    ):
        self.region = region.value
        self.jwt: dict = decompiled_jwt
        self.bovespa_account = None
        self.bmf_account = None
        self.client_id = None
        self.start_date = (datetime.now() - timedelta(days=90)).timestamp() * 1000
        self.end_date = time.time() * 1000

    def get_account(self):
        user = self.jwt.get("user", {})
        portfolios = user.get("portfolios", {})
        br_portfolios = portfolios.get("br", {})

        self.bovespa_account = br_portfolios.get("user")
        self.bmf_account = br_portfolios.get("bmf_account")
        self.client_id = user.get("unique_id")

    async def get_service_response(self) -> dict:
        self.get_account()
        if self.region == 'US':
            us_statement = await Statement.get_dw_statement(self.start_date, self.end_date)
            return self.generate_pdf(us_statement)

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
        normalized_statement = {
            'Extrato': [Statement.normalize_statement(transc) for transc in statement]
        }

        return self.generate_pdf(normalized_statement)

    def generate_pdf(self, statement: dict) -> dict:
        pdf = pdfkit.from_string(json.dumps(statement))
        file_duration = (datetime.now() - timedelta(minutes=1)).isoformat()

        RequestStatement.s3_singleton.upload_file(file_path=self.generate_path(), content=pdf,
                                                  expire_date=file_duration)
        link = RequestStatement.s3_singleton.generate_file_link(file_path=self.generate_path())
        return {"pdf_link": link}

    def generate_path(self) -> str:
        path = f"{self.client_id}/statements/{self.start_date}-{self.end_date}.pdf"
        return path
