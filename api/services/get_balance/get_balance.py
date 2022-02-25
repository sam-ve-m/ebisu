import logging

from fastapi import Request, Depends
from heimdall_client.bifrost import Heimdall

from api.application_dependencies.jwt_validator import jwt_validator_and_decompile
from api.core.interfaces.interface import IService
from api.domain.enums.region import Region
from api.utils.statement.utils import Statement

log = logging.getLogger()


class GetBalance(IService):
    oracle_singleton_instance = None

    def __init__(
            self,
            region: Region,
            decompiled_jwt: str = Depends(jwt_validator_and_decompile),
    ):
        self.region = region.value
        self.jwt = decompiled_jwt
        self.bovespa_account = None
        self.bmf_account = None

    def get_account(self):
        self.bovespa_account = self.jwt.get("bovespa_account")
        self.bmf_account = self.jwt.get("bmf_account")

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
