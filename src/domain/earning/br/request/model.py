
class QueryBrParams:
    def __init__(
            self,
            region: str,
            limit: int,
            offset: int,
            earnings_types: str = None
    ):
        self.__region = region
        self.__limit = limit
        self.__offset = offset
        self.__earnings_types = earnings_types

    def get_query_br_string_dict(self):
        query_br_string_dict = {
            "region": self.__region,
            "limit": self.__limit,
            "offset": self.__offset,
            "earnings_types": self.__earnings_types,
        }
        return query_br_string_dict


class TransactionBrRequest:

    def __init__(
        self,
        accounts: str,
        query_params: QueryBrParams
    ):
        self.__accounts: str = accounts
        self.__query_params: QueryBrParams = query_params

    def get_account(self):
        return self.__accounts

    def get_query_params(self):
        return self.__query_params.get_query_br_string_dict()
