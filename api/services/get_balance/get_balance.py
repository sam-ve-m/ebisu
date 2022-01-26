import logging

from fastapi import Request
from heimdall_client.bifrost import Heimdall

from api.core.interfaces.interface import IService
from api.domain.enums.region import Region
from api.utils.statement.utils import Statement

log = logging.getLogger()


class GetBalance(IService):
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

    async def get_service_response(self) -> dict:
        self.get_account()
        if self.region == 'US':
            balance_us = await Statement.get_dw_balance()
            return balance_us

        query = f"SELECT VL_TOTAL FROM CORRWIN.TCCSALDO WHERE CD_CLIENTE = {self.bmf_account}"
        balance = GetBalance.oracle_singleton_instance.get_data(sql=query)

        return {
            'balance': balance.pop().get("VL_TOTAL"),
        }
