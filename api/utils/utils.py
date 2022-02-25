import time
from urllib import parse


def get_query_params_rom_url(url: str):
    array_fields = ["entity_types"]
    query_params = dict(parse.parse_qsl(parse.urlsplit(url).query))
    for key, value in query_params.items():
        if key == "entity_types" or key in array_fields:
            query_params[key] = value.split("|")
    return query_params


def str_to_timestamp(date: str) -> float:
    return time.mktime(time.strptime(str(date), "%Y-%m-%d %H:%M:%S.%f"))


def str_to_timestamp_statement(date: str) -> float:
    return time.mktime(time.strptime(str(date), "%Y-%m-%d %H:%M:%S"))


def str_to_timestamp_statement_us(date: str) -> float:
    return time.mktime(time.strptime(str(date), "%Y-%m-%dT%H:%M:%S.%fZ"))


FROM_SEARCH_PARAMS_TO_ORACLE_KEYS = {
    "symbols": "SYMBOL",
    "order_status": "ORDSTATUS",
    "order_type": "ORDTYPE",
    "trade_sides": "SIDE",
    "time_in_forces": "TIMEINFORCE",
}
