from datetime import datetime
from typing import List
import pytz

from api.services.get_statement.dw_connection import DWTransport
from api.domain.time_formatter.time_formatter import (
    str_to_timestamp_statement,
    str_to_timestamp_statement_us,
)
from api.services.jwt.service import jwt_validator_and_decompile
from fastapi import Depends


class Statement:
    dw = DWTransport()

    @staticmethod
    def normalize_statement(client_statement: dict) -> dict:
        normalized_data = {
            "date": str_to_timestamp_statement(client_statement.get("DT_LANCAMENTO")),
            "description": client_statement.get("DS_LANCAMENTO"),
            "value": client_statement.get("VL_LANCAMENTO"),
        }
        return normalized_data

    @staticmethod
    def normalize_statement_us(client_statement: dict) -> List[dict]:
        statements = []
        for transaction in client_statement.get("dict_body"):
            statements.append(
                {
                    "date": str_to_timestamp_statement_us(transaction.get("tranWhen")),
                    "description": transaction.get("comment"),
                    "value": transaction.get("tranAmount"),
                }
            )
        return statements

    @staticmethod
    def normalize_splited_date_to_string(day: int, month: int, year: int):
        received_date = datetime(year, month, day)
        date = received_date.date()
        return date

    @staticmethod
    def normalize_balance_us(client_balance: dict) -> dict:
        balance = client_balance.get("dict_body").get("cash").get("cashBalance")
        return balance

    @staticmethod
    def from_timestamp_to_utc_isoformat_us(timestamp: float):
        format_date = datetime.fromtimestamp(timestamp / 1000, tz=pytz.utc).isoformat()
        return format_date

    @staticmethod
    def from_timestamp_to_utc_isoformat_br(timestamp: float):
        timestamp_miliseconds = timestamp / 1000
        raw_date = datetime.fromtimestamp(timestamp_miliseconds)
        format_date = raw_date.strftime(format="%Y-%m-%d")
        return format_date

    @staticmethod
    def get_dw_account(decompiled_jwt: dict = Depends(jwt_validator_and_decompile)):
        user = decompiled_jwt.get("user", {})
        portfolios = user.get("portifolios", {})
        us_portfolios = portfolios.get("us", {})
        dw_account_response = us_portfolios.get("dw_account")
        return dw_account_response

    @staticmethod
    async def get_dw_statement(dw_account: str, start_date: float, end_date: float, offset: int, limit: int) -> dict:
        start_date = Statement.from_timestamp_to_utc_isoformat_us(start_date)
        end_date = Statement.from_timestamp_to_utc_isoformat_us(end_date)

        raw_statement = await Statement.dw.get_transactions(
            dw_account, start=start_date, end=end_date, limit=limit
        )
        raw_balance = await Statement.dw.get_balances(dw_account)
        balance = Statement.normalize_balance_us(*raw_balance)
        statement = Statement.normalize_statement_us(*raw_statement)
        return {"balance": balance, "statements": statement}

    @staticmethod
    async def get_dw_balance():
        dw_account = Statement.get_dw_account()
        raw_balance = await Statement.dw.get_balances(dw_account)
        balance = Statement.normalize_balance_us(*raw_balance)
        return {"balance": balance}