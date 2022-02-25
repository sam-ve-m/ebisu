import logging
from decouple import config
from typing import List
from fastapi import Depends
from api.utils.pipe_to_list import pipe_to_list
from api.application_dependencies.jwt_validator import jwt_validator_and_decompile
from api.utils.utils import str_to_timestamp_statement
from api.services.get_earnings.br_earnings.strategy import GetBrEarnings
from api.utils.earnings.earnings_utils import Earnings

log = logging.getLogger()


class EarningsService:
    oracle_earnings_singleton_instance = None
    # schema oracle table - symbol | timestamp | price | type_earnings

    def __init__(self,
                 symbols: str,
                 timestamp: float,
                 offset: float,
                 limit: int,
                 decompiled_jwt: str = Depends(jwt_validator_and_decompile),
                 ):
        self.symbols = pipe_to_list(symbols)
        self.timestamp = timestamp
        self.offset = offset
        self.limit = limit
        self.decompiled_jwt = decompiled_jwt

    def get_symbols(self):
        self.symbols = self.decompiled_jwt.get("symbols")

    @staticmethod
    def normalize_earnings(client_earnings: dict) -> dict:
        normalize_data = {
            "symbol": client_earnings.get("SYMBOL"),
            "date": str_to_timestamp_statement(client_earnings.get('EARNINGS_DATE')),
            "price": client_earnings.get("PRICE"),
            "earnings_type": client_earnings.get("EARNINGS_TYPE"),
        }
        return normalize_data

    async def get_earnings_service(self) -> List[dict]:
        self.get_symbols()
        timestamp_date = Earnings.from_timestamp_to_utc_isoformat_br(self.timestamp)
        query_earnings = GetBrEarnings.build_query_earnings(self.timestamp, self.limit, self.limit)
        open_earnings = GetBrEarnings.oracle_earnings_singleton_instance.get_data(sql=query_earnings)
        return [
            EarningsService.normalize_earnings(open_earning)
            for open_earning in open_earnings
        ]
