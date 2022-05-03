from pydantic import BaseModel, constr, confloat, root_validator

from api.domain.enums.region import Region


class AccountCashFlow(BaseModel):
    account_number: constr(min_length=1)
    country: Region


class UserMoneyFlow(BaseModel):
    origin_account: AccountCashFlow
    account_destination: AccountCashFlow
    value: confloat()


class UserMoneyFloSameExchange(BaseModel):
    origin_account: AccountCashFlow
    account_destination: AccountCashFlow
    value: confloat()

    @root_validator
    def validate(cls, values):
        if values["origin_account"]["country"] != values["account_destination"]["country"]:
            raise ValueError("Accounts are not from the same country")
        return UserMoneyFlow(**values)


class UserMoneyFloDifferentExchange(BaseModel):
    origin_account: AccountCashFlow
    account_destination: AccountCashFlow
    value: confloat()

    @root_validator
    def validate(cls, values):
        if values["origin_account"]["country"] == values["account_destination"]["country"]:
            raise ValueError("Accounts are not from the same country")
        return UserMoneyFlow(**values)