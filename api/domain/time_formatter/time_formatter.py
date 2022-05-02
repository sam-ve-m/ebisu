from datetime import datetime
import time


def str_to_timestamp(date: datetime) -> float:
    return date.timestamp()


def str_to_timestamp_statement(date: str) -> float:
    return time.mktime(time.strptime(str(date), "%Y-%m-%d %H:%M:%S"))


def str_to_timestamp_statement_us(date: str) -> float:
    return time.mktime(time.strptime(str(date), "%Y-%m-%dT%H:%M:%S.%fZ"))
