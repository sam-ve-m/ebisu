from datetime import datetime
from typing import List

import pytz
from api.services.get_statement.dw_connection import DWTransport


class Statement:

    @staticmethod
    def normalize_statement(client_statement: dict) -> dict:
        normalized_data = {
            "date": str(client_statement.get('DT_LANCAMENTO')),
            "description": client_statement.get("DS_LANCAMENTO"),
            "value": client_statement.get("VL_LANCAMENTO"),
        }
        return normalized_data

    @staticmethod
    def normalize_statement_us(client_statement: dict) -> List[dict]:
        statements = []
        for transaction in client_statement.get('dict_body'):
            statements.append({
                "date": str(transaction.get('tranWhen')),
                "description": transaction.get("comment"),
                "value": transaction.get("tranAmount"),
            })
        return statements

    @staticmethod
    def normalize_balance_us(client_balance: dict) -> dict:
        balance = client_balance.get('dict_body').get('cash').get('cashBalance')
        return balance

    @staticmethod
    def from_timestamp_to_utc_isoformat_us(timestamp: float):
        format_date = datetime.fromtimestamp(timestamp / 1000, tz=pytz.utc).isoformat()
        return format_date

    @staticmethod
    def from_timestamp_to_utc_isoformat_br(timestamp: float):
        raw_date = datetime.fromtimestamp(timestamp / 1000)
        format_date = raw_date.strftime(format="%Y-%m-%d")
        return format_date

    @staticmethod
    async def get_dw_statement(start_date: float, end_date: float, limit: int = None) -> dict:
        dw = DWTransport()
        start_date = Statement.from_timestamp_to_utc_isoformat_us(start_date)
        end_date = Statement.from_timestamp_to_utc_isoformat_us(end_date)
        raw_statement = await dw.get_orders('6bf1ef07-55c9-43ce-802b-f62ad5b56337.1634935585221', start=start_date,
                                            end=end_date, limit=limit)
        raw_balance = await dw.get_balances('6bf1ef07-55c9-43ce-802b-f62ad5b56337.1634935585221')
        balance = Statement.normalize_balance_us(*raw_balance)
        statement = Statement.normalize_statement_us(*raw_statement)
        return {
                'balance': balance,
                'statement': statement
                }
