# Standards
import json
from typing import List

# Third part
from aiohttp import ClientResponse

from mepho import DWApiTransport

from src.infrastructures.env_config import config


class DWTransport:
    session = None

    def __init__(self):
        self.token = None
        self.expire_at = None

    async def get_transactions(
        self, account: str, limit: int, offset, start_date, end_date
    ) -> List[dict]:
        if not account:
            return []
        url = config("DW_GET_ALL_TRANSACTIONS_URL")
        query_params = {"offset": offset, "limit": limit, "from": start_date, "to": end_date}
        if not limit:
            del query_params["limit"]

        url_formatted = url.format(account)
        response = await DWApiTransport.execute_get(
            url=url_formatted, query_params=query_params
        )
        response = await self._response_body_in_json_and_account_id(response=response)
        return response

    async def get_balances(self, account: str) -> List[dict]:
        if not account:
            return []
        url = config("DW_BALANCE_URL")

        url_formatted = url.format(account)
        response = await DWApiTransport.execute_get(url=url_formatted, query_params={})
        response = await self._response_body_in_json_and_account_id(response=response)
        return response

    @staticmethod
    async def _response_body_in_json_and_account_id(
        response: ClientResponse,
    ) -> List[dict]:
        bodies = list()
        body = await response.text()
        dict_body = json.loads(body)
        bodies.append({"dict_body": dict_body})
        return bodies
