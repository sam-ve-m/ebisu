import asyncio
import json
import re
from typing import List

from aiohttp import ClientResponse
from etria_logger import Gladsheim
from mepho import DWApiTransport


class DWRepository:
    transport = DWApiTransport

    @classmethod
    async def get_positions_br(cls, accounts: List[str]) -> int:
        query = cls.__build_query_br(accounts)
        result = cls.positions_repository.get_one_data(query)
        positions = result.get("SUM(A.QTDE_TOT)", 0)
        return positions

    @classmethod
    async def _execute_get(
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
    async def _response_body_in_json_and_account_id(
        responses: List[ClientResponse], base_url: str
    ) -> List[dict]:
        bodies = list()
        for response in responses:
            body = await response.text()
            account = DWRepository._extract_account_from_url(
                url=str(response.url), base_url=base_url
            )
            dict_body = json.loads(body)
            bodies.append({"account": account, "dict_body": dict_body})
        return bodies

    @staticmethod
    def _extract_account_from_url(url: str, base_url: str) -> str:
        regex = base_url.replace("/", "\/").replace(".", "\.").replace("{}", "(.+)")
        if matches := re.match(regex, url):
            return matches[1]
