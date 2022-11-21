# Ebisu
from src.domain.exceptions.domain.model.thebes_answer.model import BrAccountIsBlocked, DataNotFoundInJwt


class ThebesAnswer:
    def __init__(self, jwt_data: dict):
        self.jwt_data = jwt_data

    @property
    def bmf_account(self):
        bmf_account = self.portfolios.get("br", {}).get("bmf_account")
        if not bmf_account:
            raise DataNotFoundInJwt()
        return bmf_account

    @property
    def bmf_account_digit(self):
        bmf_account = self.portfolios.get("br", {}).get("bovespa_account")
        bmf_account_digit = bmf_account[-1]
        return bmf_account_digit

    @property
    def dw_account(self):
        dw_account = self.portfolios.get("us", {}).get("dw_account")
        if not dw_account:
            raise DataNotFoundInJwt()
        return dw_account

    @property
    def dw_display_account(self):
        dw_display_account = self.portfolios.get("us", {}).get("dw_display_account")
        if not dw_display_account:
            raise DataNotFoundInJwt()
        return dw_display_account

    @property
    def portfolios(self):
        portfolios = self.jwt_data.get("user", {}).get("portfolios")
        if not portfolios:
            raise DataNotFoundInJwt()
        return portfolios

    @property
    def unique_id(self):
        unique_id = self.jwt_data.get("user", {}).get("unique_id")
        if not unique_id:
            raise DataNotFoundInJwt()
        return unique_id

    def account_br_is_blocked(self):
        account_br_is_blocked = self.jwt_data.get("user", {}).get("account_br_is_blocked")
        if account_br_is_blocked is None:
            raise DataNotFoundInJwt()

        if account_br_is_blocked:
            raise BrAccountIsBlocked()

        return account_br_is_blocked
