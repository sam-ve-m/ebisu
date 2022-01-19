from heimdall_client.bifrost import Heimdall
import logging

from orjson import orjson

from api.core.interfaces.interface import IService
from fastapi import Request, Response

from api.domain.enums.region import Region
log = logging.getLogger()


class GetStatement(IService):
    oracle_singleton_instance = None

    def __init__(
            self,
            request: Request,
            region: Region,
    ):
        self.region = region.value
        self.jwt = request.headers.get("x-thebs-answer")
        self.bovespa_account = None
        self.bmf_account = None

    def get_account(self):
        heimdall = Heimdall(logger=log)
        jwt_data = heimdall.decrypt_payload(jwt=self.jwt)
        self.bovespa_account = jwt_data.get("bovespa_account")
        self.bmf_account = jwt_data.get("bmf_account")

    async def get_service_response(self) -> Response:
        self.get_account()
        query = "SELECT DT_LANCAMENTO, DS_LANCAMENTO, VL_LANCAMENTO FROM CORRWIN.TCCMOVTO WHERE CD_CLIENTE = 78"
        data = GetStatement.oracle_singleton_instance.get_data(sql=query)
        query = "SELECT VL_TOTAL FROM CORRWIN.TCCSALDO WHERE CD_CLIENTE = 78"
        balance = GetStatement.oracle_singleton_instance.get_data(sql=query)
        return Response(media_type="application/json", content=orjson.dumps({'balance': balance.pop().get("VL_TOTAL"), 'statament': [transc for transc in data]}))