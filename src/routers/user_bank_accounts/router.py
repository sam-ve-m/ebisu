from fastapi import Request, APIRouter, Depends

# INTERNAL LIBS
from nidavellir import Sindri
from src.core.interfaces.bank_transfer.interface import IBankTransfer
from src.services.device_info.service import DeviceInfoService
from src.services.get_bank_code.service import GetBankCode
from src.domain.request.user_account.bank_account import (
    CreateUserBankAccount,
    UpdateUserBankAccounts,
    DeleteUsersBankAccount,
)
from src.domain.models.response.create_bank_account.response_model import (
    ListBankAccountsResponse,
)

# SERVICES
from src.services.bank_account.service import UserBankAccountService
from src.services.bank_transfer.service import BankTransferService
from src.services.jwt.service import JwtService


class UserBankAccountsRouter:

    __bank_account_router = APIRouter()

    @staticmethod
    def get_user_account_router():
        return UserBankAccountsRouter.__bank_account_router

    @staticmethod
    @__bank_account_router.get(
        "/user/list_bank_accounts",
        tags=["User Bank Account"],
        response_model=ListBankAccountsResponse,
    )
    async def get_user_bank_accounts(request: Request):
        jwt_data = await JwtService.validate_and_decode_thebes_answer(request=request)
        jwt_data = {"x-thebes-answer": jwt_data}
        user_bank_accounts = await UserBankAccountService.get_user_bank_accounts(
            jwt_data
        )
        return user_bank_accounts

    @staticmethod
    @__bank_account_router.post("/user/create_bank_account", tags=["User Bank Account"])
    async def create_user_bank_accounts(
        request: Request, create_bank_account: CreateUserBankAccount
    ):
        jwt_data = await JwtService.validate_and_decode_thebes_answer(request=request)

        jwt_data = {
            "x-thebes-answer": jwt_data,
            "bank_account": create_bank_account.dict(),
        }
        device_info = await DeviceInfoService.get_device_info(request)
        create_user_bank_accounts_response = (
            await UserBankAccountService.create_user_bank_accounts(
                jwt_data=jwt_data,
                device_info=device_info,
            )
        )
        return create_user_bank_accounts_response

    @staticmethod
    @__bank_account_router.put("/user/update_bank_account", tags=["User Bank Account"])
    async def update_bank_account(
        request: Request, update_bank_account: UpdateUserBankAccounts
    ):
        jwt_data = await JwtService.validate_and_decode_thebes_answer(request=request)

        bank_account = update_bank_account.dict()
        Sindri.dict_to_primitive_types(obj=bank_account)
        jwt_data = {
            "x-thebes-answer": jwt_data,
            "bank_account": bank_account,
        }
        device_info = await DeviceInfoService.get_device_info(request)
        update_bank_account_response = (
            await UserBankAccountService.update_user_bank_account(
                jwt_data=jwt_data,
                device_info=device_info,
            )
        )
        return update_bank_account_response

    @staticmethod
    @__bank_account_router.delete(
        "/user/delete_bank_account", tags=["User Bank Account"]
    )
    async def delete_bank_account(
        request: Request, delete_bank_account: DeleteUsersBankAccount
    ):
        jwt_data = await JwtService.validate_and_decode_thebes_answer(request=request)

        bank_account = delete_bank_account.dict()
        jwt_data = {"x-thebes-answer": jwt_data, "bank_account": bank_account}
        device_info = await DeviceInfoService.get_device_info(request)
        delete_bank_account_response = (
            await UserBankAccountService.delete_user_bank_account(
                jwt_data=jwt_data,
                device_info=device_info,
            )
        )
        return delete_bank_account_response

    @staticmethod
    @__bank_account_router.get("/transfer", tags=["Bank Transfer"])
    async def bank_transfer(
        request: Request, service: IBankTransfer = Depends(BankTransferService)
    ):
        bank_transfer_account_response = await service.get_bank_transfer_account(
            request
        )
        return bank_transfer_account_response

    @staticmethod
    @__bank_account_router.get("/bank_code", tags=["Bank Code"])
    def bank_code_and_description():

        response = GetBankCode.get_service_response()
        return response
