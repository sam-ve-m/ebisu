# STANDARD LIBS
from datetime import datetime
from typing import List
import pytz

# INTERNAL LIBS
from src.domain.time_formatter.time_formatter import (
    str_to_timestamp_statement_us,
)
from src.transport.drive_wealth.statement.transport import DwStatementTransport


class Statement:

    @staticmethod
    def from_timestamp_to_utc_isoformat_us(timestamp: float):
        format_date = datetime.fromtimestamp(timestamp / 1000, tz=pytz.utc)
        US_DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
        execution_date_time = datetime.strftime(format_date, US_DATE_TIME_FORMAT)
        return execution_date_time

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
    async def get_dw_statement(
        dw_account: str, offset: int, limit: int, from_date: int, to_date: int
    ) -> dict:

        from_date = Statement.from_timestamp_to_utc_isoformat_us(from_date)
        to_date = Statement.from_timestamp_to_utc_isoformat_us(to_date)
        offset_date = Statement.from_timestamp_to_utc_isoformat_us(offset)

        raw_transactions = await DwStatementTransport.get_transactions(
            dw_account, limit=limit, offset=offset_date, from_date=from_date, to_date=to_date
        )
        raw_balance = await DwStatementTransport.get_balances(dw_account)
        # TODO INTERNAL SERVER ERROR
        balance = Statement.normalize_balance_us(*raw_balance)
        statement = Statement.normalize_statement_us(*raw_transactions)
        return {"balance": balance, "statements": statement}

    @staticmethod
    def normalize_balance_us(client_balance: dict) -> dict:
        balance = client_balance.get("dict_body").get("cash").get("cashBalance")
        return balance

    # TODO: Verificar como remover essa parada
    @staticmethod
    async def get_dw_balance(dw_account: str):
        raw_balance = await DwStatementTransport.get_balances(dw_account)
        balance = Statement.normalize_balance_us(*raw_balance)
        return {"balance": balance}
