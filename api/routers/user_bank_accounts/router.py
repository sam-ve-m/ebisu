from api.core.interfaces.bank_transfer.interface import IBankTransfer
from fastapi import Request, APIRouter, Depends

from api.services.bank_account.service import UserBankAccountService
from api.services.bank_transfer.service import BankTransferService
from api.services.jwt.service_jwt import JwtService


class UserBankAccountsRouter:

    __bank_account_router = APIRouter()

    @staticmethod
    def get_user_account_router():
        return UserBankAccountsRouter.__bank_account_router

    @staticmethod
    @__bank_account_router.get("/user/list_bank_accounts", tags=["User Bank Account"])
    async def get_user_bank_accounts(request: Request):
        jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
        get_user_bank_accounts_response = await UserBankAccountService.get_user_bank_accounts(jwt_data=jwt_data)
        return get_user_bank_accounts_response

    @__bank_account_router.post("/user/create_bank_account", tags=["User Bank Account"])
    async def create_user_bank_accounts(request: Request):
        jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
        create_user_bank_accounts_response = await UserBankAccountService.create_user_bank_accounts(jwt_data=jwt_data)
        return create_user_bank_accounts_response

    @__bank_account_router.put("/user/update_bank_account", tags=["User Bank Account"])
    async def update_bank_account(request: Request):
        jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
        update_bank_account_response = await UserBankAccountService.update_user_bank_account(jwt_data=jwt_data)
        return update_bank_account_response

    @__bank_account_router.delete("/user/delete_bank_account", tags=["User Bank Account"])
    async def delete_bank_account(request: Request):
        jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
        delete_bank_account_response = await UserBankAccountService.delete_user_bank_account(jwt_data=jwt_data)
        return delete_bank_account_response

    @__bank_account_router.get("/transfer", tags=["Bank Transfer"])
    async def bank_transfer(
            request: Request, service: IBankTransfer = Depends(BankTransferService)
    ):
        bank_transfer_account_response = await service.get_bank_transfer_account(request)
        return bank_transfer_account_response
