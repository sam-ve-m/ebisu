from pydantic import BaseModel, constr, confloat, root_validator, UUID4
from src.domain.enums.region import Region


class AccountCashFlow(BaseModel):
    account_number: constr(min_length=1)
    country: Region


class UserMoneyFlowSameExchange(BaseModel):
    origin_account: AccountCashFlow
    account_destination: AccountCashFlow
    value: confloat()

    @root_validator
    def validate_oring_account(cls, values):
        if (
            values["origin_account"]["country"]
            != values["account_destination"]["country"]
        ):
            raise ValueError("Accounts are not from the same country")
        return values


class UserMoneyFlowDifferentExchange(BaseModel):
    origin_account: AccountCashFlow
    account_destination: AccountCashFlow
    value: confloat()

    @root_validator
    def validate_oring_account(cls, values):
        if (
            values["origin_account"]["country"]
            == values["account_destination"]["country"]
        ):
            raise ValueError("Accounts are not from the same country")
        return values


class UserMoneyFlowToExternalBank(BaseModel):
    bank_account_id: UUID4
    value: confloat()
