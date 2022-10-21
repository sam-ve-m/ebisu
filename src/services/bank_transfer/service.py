# STANDARD LIBS
from fastapi import Request

# INTERNAL LIBS
from src.core.interfaces.bank_transfer.interface import IBankTransfer
from src.infrastructures.env_config import config
from src.services.jwt.service import JwtService


class BankTransferService(IBankTransfer):
    @staticmethod
    async def get_bank_transfer_account(request: Request):

        user_jwt = await JwtService.validate_and_decode_thebes_answer(request)

        user_response = {
            "agency": "0001",
            "bank": config("BANK_CODE"),
            "account": user_jwt
            .get("user", {})
            .get("portfolios", {})
            .get("br", {})
            .get("bovespa_account"),
        }

        return user_response
