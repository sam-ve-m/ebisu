from pydantic import BaseModel, constr, confloat

from api.domain.enums.region import Region


class AccountCashFlow(BaseModel):
    account_number: constr(min_length=1)
    country: Region


class UserMoneyFlow(BaseModel):
    origin_account: AccountCashFlow
    account_destination: AccountCashFlow
    value: confloat()
