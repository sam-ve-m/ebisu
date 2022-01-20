from datetime import datetime
from typing import List

from heimdall_client.bifrost import Heimdall
import logging

from orjson import orjson

from api.core.interfaces.interface import IService
from fastapi import Request, Response

from api.domain.enums.region import Region
from api.services.get_statement.dw_connection import DWTransport

log = logging.getLogger()


class GetStatement(IService):
    oracle_singleton_instance = None

    def __init__(
            self,
            request: Request,
            region: Region,
            start_date: datetime,
            end_date: datetime
    ):
        self.region = region.value
        self.jwt = request.headers.get("x-thebs-answer")
        self.bovespa_account = None
        self.bmf_account = None
        self.start_date = start_date.strftime(format="%Y-%m-%d")
        self.end_date = end_date.strftime(format="%Y-%m-%d")

    def get_account(self):
        heimdall = Heimdall(logger=log)
        jwt_data = heimdall.decrypt_payload(jwt=self.jwt)
        self.bovespa_account = jwt_data.get("bovespa_account")
        self.bmf_account = jwt_data.get("bmf_account")

    @staticmethod
    def normalize_statement(client_statement: dict) -> dict:
        normalized_data = {
            "date": client_statement.get('DT_LANCAMENTO'),
            "description": client_statement.get("DS_LANCAMENTO"),
            "value": client_statement.get("VL_LANCAMENTO"),
        }
        return normalized_data

    @staticmethod
    def normalize_statement_us(client_statement: List[dict]) -> dict:
        statements = []
        for transaction in client_statement.get('dict_body'):
            print(transaction)
            statements.append({
                "date": transaction.get('tranWhen'),
                "description": transaction.get("comment"),
                "value": transaction.get("tranAmount"),
            })
        return statements

    async def get_service_response(self) -> dict:
        self.get_account()
        query = f"""SELECT DT_LANCAMENTO, DS_LANCAMENTO, VL_LANCAMENTO 
                   FROM CORRWIN.TCCMOVTO 
                   WHERE CD_CLIENTE = {self.bmf_account} 
                   AND DT_LANCAMENTO > TO_DATE('{self.start_date}', 'yyyy-MM-dd')
                   AND DT_LANCAMENTO <= TO_DATE('{self.end_date}', 'yyyy-MM-dd')
                   ORDER BY DT_LANCAMENTO
                   """
        statement = GetStatement.oracle_singleton_instance.get_data(sql=query)
        query = f"SELECT VL_TOTAL FROM CORRWIN.TCCSALDO WHERE CD_CLIENTE = {self.bmf_account}"
        balance = GetStatement.oracle_singleton_instance.get_data(sql=query)
        if self.region == 'US':
            us_statement = await self.get_dw_statement()
            return GetStatement.normalize_statement_us(*us_statement)
        return {'balance': balance.pop().get("VL_TOTAL"),
                'statament': [GetStatement.normalize_statement(transc) for transc in statement]}

    async def get_dw_statement(self):
        dw = DWTransport()
        statement = await dw.get_orders('6bf1ef07-55c9-43ce-802b-f62ad5b56337.1634935585221')
        return statement