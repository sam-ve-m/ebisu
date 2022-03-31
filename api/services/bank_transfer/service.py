from api.core.interfaces.bank_transfer.interface import IBankTransfer
from api.infrastructures.env_config import config
from api.services.jwt.service import jwt_validator_and_decompile
from fastapi import Request


class BankTransferService(IBankTransfer):
    @staticmethod
    async def get_bank_transfer_account(request: Request):

        user_jwt = await jwt_validator_and_decompile(request)
        return {
            "agency": "0001",
            "bank": config("BANK_CODE"),
            "account": user_jwt.get("user", {})
            .get("portfolios", {})
            .get("br", {})
            .get("bovespa_account"),
        }
