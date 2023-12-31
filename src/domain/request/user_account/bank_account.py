from pydantic import BaseModel, UUID4, validator, constr
from typing import Optional

from src.domain.exceptions.domain.request.user_account.model import InvalidBankCode
from src.domain.request.device_info import DeviceInformationOptional
from src.services.bank_account.service import UserBankAccountService


class BankCode(BaseModel):
    bank: str

    @validator("bank", check_fields=True, always=True, allow_reuse=True)
    def validate_whether_bank_code_exists(cls, e):
        if not UserBankAccountService.bank_code_from_client_exists(bank=e):
            raise InvalidBankCode()
        return e


class CreateUserBankAccount(BankCode):
    bank: str
    account_type: str
    agency: constr(max_length=5)
    account_number: str
    account_name: Optional[str]


class UpdateUserBankAccounts(BankCode):
    bank: Optional[str]
    account_type: Optional[str]
    agency: Optional[constr(max_length=5)]
    account_number: Optional[str]
    account_name: Optional[str]
    id: UUID4


class DeleteUsersBankAccount(BaseModel):
    id: str


class GetUserBankAccount(BaseModel):
    unique_id: str
