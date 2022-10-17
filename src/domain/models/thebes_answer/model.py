# Ebisu
from src.domain.exceptions.domain.forex.model import DataNotFoundInJwt


class ThebesAnswer:
    def __init__(self, jwt_data: dict):
        self.jwt_data = jwt_data
        self.unique_id = self.__get_unique_id()
        self.portfolios = self.__get_portfolios()
        self.bmf_account = self.__get_bmf_account()
        self.dw_account = self.__get_dw_account()
        self.dw_display_account = self.__get_dw_display_account()

    def __get_bmf_account(self):
        bmf_account = self.portfolios.get("br", {}).get("bmf_account")
        if not bmf_account:
            raise DataNotFoundInJwt()
        return bmf_account

    def __get_dw_account(self):
        dw_account = self.portfolios.get("us", {}).get("dw_account")
        if not dw_account:
            raise DataNotFoundInJwt()
        return dw_account

    def __get_dw_display_account(self):
        dw_display_account = self.portfolios.get("us", {}).get("dw_display_account")
        if not dw_display_account:
            raise DataNotFoundInJwt()
        return dw_display_account

    def __get_portfolios(self):
        portfolios = self.jwt_data.get("user", {}).get("portfolios")
        if not portfolios:
            raise DataNotFoundInJwt()
        return portfolios

    def __get_unique_id(self):
        unique_id = self.jwt_data.get("user", {}).get("unique_id")
        if not unique_id:
            raise DataNotFoundInJwt()
        return unique_id

    def account_br_is_blocked(self):
        account_br_is_blocked = self.jwt_data.get("user", {}).get("account_br_is_blocked")
        if account_br_is_blocked is None:
            raise DataNotFoundInJwt()

        if account_br_is_blocked is False:
            raise



        return account_br_is_blocked
