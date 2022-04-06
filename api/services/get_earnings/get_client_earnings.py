from typing import List

from api.repositories.earnings.repository import EarningsRepository
from api.services.get_earnings.strategies.br_earnings import earnings_regions
from api.services.get_earnings.strategies.service import Earnings


class EarningsService:
    oracle_earnings_singleton_instance = EarningsRepository

    @classmethod
    def normalize_earnings(cls, client_earnings: dict) -> dict:
        normalize_data = {
            "symbol": client_earnings.get("SYMBOL"),
            "date": client_earnings.get("EARNINGS_DATE"),
            "price": client_earnings.get("PRICE"),
            "earnings_type": client_earnings.get("EARNINGS_TYPE"),
        }
        return normalize_data

    @classmethod
    async def get_service_response(
            cls, symbol: str, timestamp: float, limit: int, offset: int
    ) -> List[dict]:
        earnings_region = earnings_regions.get("BR")
        query_earnings = earnings_region.build_query_earnings(
            symbol=symbol,
            timestamp=Earnings.from_timestamp_to_utc_isoformat_br(timestamp),
            limit=limit,
            offset=offset,
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
