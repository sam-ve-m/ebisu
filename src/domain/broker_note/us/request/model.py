class ConfimationQueryParams:
    def __init__(
        self,
        from_date: str,
        to_date: str,
    ):
        self.__from_date = from_date
        self.__to_date = to_date

    def get_query_string_dict(self):
        query_string_dict = {
            "from": self.__from_date,
            "to": self.__to_date,
        }
        return query_string_dict


class ConfirmationRequest:
    def __init__(self, account: str, query_params: ConfimationQueryParams):
        self.__account: str = account
        self.__query_params: ConfimationQueryParams = query_params

    def get_account(self):
        return self.__account

    def get_query_params(self):
        return self.__query_params.get_query_string_dict()


class GetStatementRequest:
    def __init__(self, account: str, file_key: str):
        self.__account: str = account
        self.__file_key = file_key

    def get_account(self):
        return self.__account

    def get_file_key(self):
        return self.__file_key
