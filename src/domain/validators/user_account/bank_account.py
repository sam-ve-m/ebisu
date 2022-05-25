from pydantic import BaseModel, UUID4, validator
from typing import Optional
from src.domain.validators.user_account.onboarding_validators import Cpf
from src.exceptions.exceptions import BadRequestError
from src.repositories.bank_account.repository import UserBankAccountRepository


class BankCode(BaseModel):
    bank: str

    @validator("bank", check_fields=False, always=True, allow_reuse=True)
    def validate_whether_bank_code_exists(cls, e):
        user_repository = UserBankAccountRepository
        if not user_repository.bank_code_from_client_exists(bank=e):
            raise BadRequestError("bank_code.invalid_bank_code")


class CreateUserBankAccount(Cpf, BankCode):
    bank: str
    account_type: str
    agency: str
    account_number: str
    account_name: Optional[str]


class UpdateUserBankAccounts(BankCode):
    bank: Optional[str]
    account_type: Optional[str]
    agency: Optional[str]
    account_number: Optional[str]
    account_name: str
    id: UUID4


class DeleteUsersBankAccount(BaseModel):
    id: str


class GetUserBankAccount(BaseModel):
    unique_id: str
