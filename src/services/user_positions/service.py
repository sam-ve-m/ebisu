import asyncio
import json
import re
from typing import List

from aiohttp import ClientResponse
from etria_logger import Gladsheim
from mepho import DWApiTransport

from src.domain.enums.region import Region
from src.infrastructures.env_config import config
from src.repositories.user_positions.repository import UserPositionsRepository


class UserPositionsService:
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
        responses = await cls.__execute_get(url=url, accounts=accounts, query_params={})
        bodies = await cls.__response_body_in_json_and_account_id(
            responses=responses, base_url=url
        )
        positions = await cls.__consolidate_positions(responses_bodies=bodies)
        return len(positions)

    @classmethod
    async def __execute_get(
        cls, url, accounts: List[str], query_params: dict
    ) -> List[ClientResponse]:
        future_request = list()
        for account in accounts:
            url_formatted = url.format(account)
            future_request.append(
                cls.transport.execute_get(url=url_formatted, query_params=query_params)
            )
        responses = await asyncio.gather(*future_request)
        ok_responses = list(filter(lambda x: x.status == 200, responses))
        not_ok_responses = list(filter(lambda x: x.status != 200, responses))
        if not_ok_responses:
            Gladsheim.error(
                message=f"DWTransportGraphicAccount::execute_get::Erros to get data from dw {responses}"
            )
        return ok_responses

    @staticmethod
    async def __response_body_in_json_and_account_id(
        responses: List[ClientResponse], base_url: str
    ) -> List[dict]:
        bodies = list()
        for response in responses:
            body = await response.text()
            account = UserPositionsService.__extract_account_from_url(
                url=str(response.url), base_url=base_url
            )
            dict_body = json.loads(body)
            bodies.append({"account": account, "dict_body": dict_body})
        return bodies

    @staticmethod
    def __extract_account_from_url(url: str, base_url: str) -> str:
        regex = base_url.replace("/", "\/").replace(".", "\.").replace("{}", "(.+)")
        if matches := re.match(regex, url):
            return matches[1]

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
