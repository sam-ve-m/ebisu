import logging
from typing import List

from fastapi import Depends

from api.services.jwt.service import jwt_validator_and_decompile

from api.repositories.earnings.repository import EarningsRepository
from api.services.get_earnings.strategies.br_earnings import earnings_regions
from api.services.earnings.service import Earnings


log = logging.getLogger()


class EarningsService:
    oracle_earnings_singleton_instance = EarningsRepository

    def __init__(
        self,
        symbol: str,
        timestamp: float,
        offset: float,
        limit: int,
        decompiled_jwt: str = Depends(jwt_validator_and_decompile),
    ):
        self.symbol = symbol
        self.timestamp = timestamp
        self.offset = offset
        self.limit = limit
        self.decompiled_jwt = decompiled_jwt

    def get_symbols(self):
        self.symbol = self.decompiled_jwt.get("symbol")

    @staticmethod
    def normalize_earnings(client_earnings: dict) -> dict:
        normalize_data = {
            "symbol": client_earnings.get("SYMBOL"),
            "date": client_earnings.get("EARNINGS_DATE"),
            "price": client_earnings.get("PRICE"),
            "earnings_type": client_earnings.get("EARNINGS_TYPE"),
        }
        return normalize_data

    async def get_service_response(self) -> List[dict]:
        earnings_region = earnings_regions.get("BR")
        query_earnings = earnings_region.build_query_earnings(
            symbol=self.symbol,
            timestamp=Earnings.from_timestamp_to_utc_isoformat_br(self.timestamp),
            limit=self.limit,
            offset=self.offset,
        )
        open_earnings = earnings_region.oracle_earnings_singleton_instance.get_data(
            sql=query_earnings
        )
        open_earnings_data = [
            EarningsService.normalize_earnings(open_earning)
            for open_earning in open_earnings
        ]
        if not open_earnings_data:
            return [{}]
        return open_earnings_data
