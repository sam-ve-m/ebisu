from datetime import datetime

import pytz

from src.domain.statement.br.model.region_date_format.enum import RegionDateFormat


class QueryParams:
    def __init__(
        self,
        from_date: int,
        to_date: int,
        offset: int,
        limit: int,
        region_date_format: RegionDateFormat
    ):
        self.__from_date = from_date
        self.__to_date = self.__get_us_string_datetime_from_timestamp(to_date, region_date_format)
        self.__offset = self.__get_us_string_datetime_from_timestamp(offset, region_date_format)
        self.__limit = self.__get_us_string_datetime_from_timestamp(limit, region_date_format)

    @staticmethod
    def __get_us_string_datetime_from_timestamp(timestamp: int, region_date_forma: RegionDateFormat):
        format_date = datetime.fromtimestamp(timestamp / 1000, tz=pytz.utc)
        us_string_datetime = datetime.strftime(format_date, region_date_forma.value)
        return us_string_datetime

    def get_query_string_dict(self):
        query_string_dict = {
            "from": self.__from_date,
            "to": self.__to_date,
            "offset": self.__offset,
            "limit": self.__limit,
        }

        return query_string_dict


class TransactionRequest:

    def __init__(
        self,
        account: str,
        query_params: QueryParams
    ):
        self.__account: str = account
        self.__query_params: QueryParams = query_params

    def get_account(self):
        return self.__account

    def get_query_params(self):
        return self.__query_params.get_query_string_dict()
