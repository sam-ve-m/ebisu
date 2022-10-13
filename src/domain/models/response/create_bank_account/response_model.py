from src.domain.models.database.bank_account.model import BankAccountModel

from typing import List, Optional, TypeVar
from pydantic import BaseModel


class CreateBankAccount(BaseModel):
    bank: Optional[int]
    account_type: Optional[str]
    agency: Optional[int]
    account_number: Optional[str]
    account_name: Optional[str]
    id: Optional[str]
    status: Optional[str]


class ListBankAccountsResponse(BaseModel):
    bank_accounts: List[CreateBankAccount]

    @classmethod
    def to_response(cls, models: List[BankAccountModel]):
        bank_accounts = [
            CreateBankAccount(
                bank=model.bank,
                account_type=model.account_type,
                agency=model.agency,
                account_number=model.account_number,
                account_name=model.account_name,
                id=model.id,
                status=model.status,
            )
            for model in models
        ]
        response = cls(bank_accounts=bank_accounts)
        return response
