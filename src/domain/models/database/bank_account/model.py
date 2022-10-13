from typing import Optional
from pydantic import BaseModel
from dataclasses import dataclass


class BankAccountModel(BaseModel):
    bank: Optional[str]
    account_type: Optional[str]
    agency: Optional[int]
    account_number: Optional[str]
    account_name: Optional[str]
    id: Optional[str]
    status: Optional[str]
