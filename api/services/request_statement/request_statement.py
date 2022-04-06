import json
import time
from datetime import datetime, timedelta

import pdfkit
from api.domain.enums.region import Region
from api.repositories.files.repository import FileRepository
from api.repositories.statements.repository import StatementsRepository
from api.services.statement.service import Statement
from api.domain.exception.model import NoPdfFoundError, NoPathFoundError


class RequestStatement:
    oracle_singleton_instance = StatementsRepository
    s3_singleton = FileRepository
    end_date = None
    offset = None
    start_date = None
    bmf_account = None

    @classmethod
    async def get_service_response(
            cls,
            region: Region,
            jwt_data: dict,
            start_date: float = (datetime.now() - timedelta(days=90)).timestamp() * 1000,
            end_date: float = time.time() * 1000,
    ) -> dict:
        user = jwt_data.get("user", {})
        portfolios = user.get("portfolios", {})
        br_portfolios = portfolios.get("br", {})
        cls.bovespa_account = br_portfolios.get("bovespa_account")
        cls.bmf_account = br_portfolios.get("bmf_account")
        cls.client_id = jwt_data.get("email")

        if region == "US":
            us_statement = await Statement.get_dw_statement(
                cls.start_date, cls.end_date, cls.offset, cls.end_date
            )
            return cls.generate_pdf(us_statement)

        start_date = Statement.from_timestamp_to_utc_isoformat_br(start_date)
        end_date = Statement.from_timestamp_to_utc_isoformat_br(end_date)
        query = f"""SELECT DT_LANCAMENTO, DS_LANCAMENTO, VL_LANCAMENTO 
                   FROM CORRWIN.TCCMOVTO 
                   WHERE CD_CLIENTE = {cls.bmf_account} 
                   AND DT_LANCAMENTO > TO_DATE('{start_date}', 'yyyy-MM-dd')
                   AND DT_LANCAMENTO <= TO_DATE('{end_date}', 'yyyy-MM-dd')
                   ORDER BY DT_LANCAMENTO
                   """
        statement = RequestStatement.oracle_singleton_instance.get_data(sql=query)
        normalized_statement = {
            "Extrato": [Statement.normalize_statement(transc) for transc in statement]
        }

        return cls.generate_pdf(normalized_statement)

    @classmethod
    def generate_pdf(cls, statement: dict, client_id, start_date, end_date) -> dict:
        pdf = pdfkit.from_string(json.dumps(statement))
        file_duration = (datetime.now() - timedelta(minutes=1)).isoformat()

        RequestStatement.s3_singleton.upload_file(
            file_path=cls.generate_path(
                client_id=client_id, start_date=start_date, end_date=end_date
            ), content=pdf, expire_date=file_duration
        )
        link = RequestStatement.s3_singleton.generate_file_link(
            file_path=cls.generate_path(
                client_id=client_id, start_date=start_date, end_date=end_date)
        )
        link_pdf = {"pdf_link": link}
        if not link:
            raise Exception(NoPdfFoundError)

        return link_pdf

    @classmethod
    def generate_path(cls, client_id, start_date: float, end_date: float) -> str:
        path = f"{client_id}/statements/{start_date}-{end_date}.pdf"
        if path:
            return path

        raise Exception(NoPathFoundError)
