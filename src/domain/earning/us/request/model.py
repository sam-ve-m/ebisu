# PROJECT IMPORTS
from src.domain.date_formatters.region.timestamp.model import RegionTimeStamp


class QueryParams:
    def __init__(
        self, from_date: RegionTimeStamp, to_date: RegionTimeStamp, limit: int
    ):
        self.__from_date = from_date
        self.__to_date = to_date
        self.__limit = limit

    def get_query_string_dict(self):
        query_string_dict = {
            "from": self.__from_date.get_region_string_datetime_from_timestamp(),
            "to": self.__to_date.get_region_string_datetime_from_timestamp(),
            "limit": self.__limit,
        }

        return query_string_dict


class TransactionRequest:
    def __init__(self, account: str, query_params: QueryParams):
        self.__account: str = account
        self.__query_params: QueryParams = query_params

    def get_account(self):
        return self.__account

    def get_query_params(self):
        return self.__query_params.get_query_string_dict()
