from api.core.interfaces.bank_transfer.interface import IBankTransfer
from api.infrastructures.env_config import config
from api.services.jwt.service import jwt_validator_and_decompile
from fastapi import Request,Depends

 
class BankTransferService(IBankTransfer):

      def __init__(self,decompiled_jwt: dict = Depends(jwt_validator_and_decompile)):
        self.jwt = decompiled_jwt
      
      async def get_bank_transfer_account(self, request:Request):
        
        user_jwt = self.jwt.jwt_validator_and_decompile(request)
        return {"agency": "0001", "bank": config("BANK_CODE"), "account": user_jwt.get("user", {}).get("portfolios", {}).get("br", {}).get("bovespa_account")}