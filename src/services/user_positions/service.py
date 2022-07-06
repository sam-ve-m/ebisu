import asyncio
import json
import re
from typing import List

from aiohttp import ClientResponse
from etria_logger import Gladsheim
from mepho import DWApiTransport

from src.domain.enums.region import Region
from src.infrastructures.env_config import config
from src.repositories.drive_wealth.repository import DWRepository
from src.repositories.user_positions.repository import UserPositionsRepository


class UserPositionsService(DWRepository):
    positions_repository = UserPositionsRepository
    transport = DWApiTransport

    @staticmethod
    def __build_query_br(accounts: List[str]) -> str:
        query = """
                    SELECT
                    sum(A.QTDE_TOT)
                    FROM CORRWIN.VCFPOSICAO A
                    WHERE A.COD_CLI IN ('{}')
                """.format(
            "','".join(accounts)
        )
        return query

    @classmethod
    async def get_positions_by_region(cls, region: str, accounts: List[str]):
        get_positions_per_region = {
            Region.BR.value: cls.get_positions_br,
            Region.US.value: cls.get_positions_us,
        }
        get_position = get_positions_per_region.get(region)
        positions = await get_position(accounts)
        return positions

    @classmethod
    async def get_positions_br(cls, accounts: List[str]) -> int:
        query = cls.__build_query_br(accounts)
        result = cls.positions_repository.get_one_data(query)
        positions = result.get("SUM(A.QTDE_TOT)", 0)
        return positions

    @classmethod
    async def get_positions_us(cls, accounts: List[str]):
        if not accounts:
            return 0
        url = config("DW_POSITIONS_URL")
        responses = await cls._execute_get(url=url, accounts=accounts, query_params={})
        bodies = await cls._response_body_in_json_and_account_id(
            responses=responses, base_url=url
        )
        positions = await cls.__consolidate_positions(responses_bodies=bodies)
        return len(positions)

    @staticmethod
    async def __consolidate_positions(responses_bodies: List[dict]):
        positions = list()
        for responses_body in responses_bodies:
            try:
                account = responses_body["account"]
                dw_positions = responses_body["dict_body"]["equityPositions"]
                for dw_position in dw_positions:
                    positions.append(
                        {
                            "account": account,
                            "symbol": dw_position["symbol"],
                            "quantity": dw_position["openQty"],
                            "average_price": dw_position["avgPrice"],
                        }
                    )
            except Exception as exception:
                Gladsheim.error(
                    message=f"DWTransportGraphicAccount::__consolidate_positions::Error to fetch transaction {responses_body}:  {exception}",
                    error=exception,
                )
        return positions
