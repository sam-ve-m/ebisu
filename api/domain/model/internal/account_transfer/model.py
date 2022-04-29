from api.domain.enums.region import Region


class AccountTransfer:

    def __init__(
        self,
        account_number: str,
        country: Region,
        user_portfolios
    ):
        self.account_number = account_number
        self.country = country.value
        self.user_portfolios = user_portfolios
        self.__is_owned_by_user = False
        self.__is_primary_account = None

    def validate_accounts_ownership(self):
        accounts = list()
        for accounts_classification, accounts_by_region in self.user_portfolios.items():
            if accounts_representation := accounts_by_region.get(self.country):
                if accounts_classification == "default":
                    accounts += accounts_representation.value()
                elif accounts_classification == "vnc":
                    for account_struct in accounts_representation:
                        accounts += account_struct.value()

        for account_type, account_number in accounts.items():
            if account_number == self.account_number:
                self.__is_owned_by_user = True
                self.__is_primary_account = True

    def get_account_transfer_finger_print