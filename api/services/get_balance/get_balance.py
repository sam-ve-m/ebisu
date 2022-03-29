import logging

from fastapi import Depends

from api.services.jwt.service import jwt_validator_and_decompile
from api.core.interfaces.interface import IService
from api.domain.enums.region import Region
from api.repositories.statements.repository import StatementsRepository
from api.services.statement.service import Statement
from api.exceptions.exceptions import NotFoundError


log = logging.getLogger()


class GetBalance(IService):
    oracle_singleton_instance = StatementsRepository

    def __init__(
            self,
            region: Region,
            decompiled_jwt: dict = Depends(jwt_validator_and_decompile),
    ):
        self.region = region.value
        self.jwt: dict = decompiled_jwt
        self.bovespa_account = None
        self.bmf_account = None

    def get_account(self):
        user = self.jwt.get("user", {})
        portfolios = user.get("portfolios", {})
        br_portfolios = portfolios.get("br", {})
        self.bovespa_account = br_portfolios.get("bovespa_account")
        self.bmf_account = br_portfolios.get("bmf_account")

        self.bovespa_account = br_portfolios.get("user")
        self.bmf_account = br_portfolios.get("bmf_account")

    async def get_service_response(self) -> dict:
        self.get_account()
        if self.region == 'US':
            balance_us = await Statement.get_dw_balance()
            return balance_us

        query = f"SELECT VL_TOTAL FROM CORRWIN.TCCSALDO WHERE CD_CLIENTE = {self.bmf_account}"
        balance = GetBalance.oracle_singleton_instance.get_data(sql=query)

        if not balance:
            return {}
        return {
            'balance': balance.pop().get("VL_TOTAL"),
        }
