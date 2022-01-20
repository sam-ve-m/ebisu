# Standards
import re
import asyncio
from datetime import datetime
from typing import List
from collections.abc import AsyncIterable, Iterable
import json
# Third part
from aiohttp import ClientSession, ClientResponse


from api.utils.env_config import config


class DWTransport:
    session = None

    def __init__(self):
        self.token = None
        self.expire_at = None

    async def get_orders(
        self, account: str
    ) -> List[dict]:
        if not account:
            return []
        url = config("DW_GET_ALL_TRANSACTIONS_URL")
        query_params = {
            "from": '2022-01-01T19:46:58.790Z',
            "to": '2022-01-20T19:46:58.790Z',
        }
        response = await self.execute_get_with_auth(
            url=url, account=account, query_params=query_params
        )

        return response

    async def get_balances(self, account: str) -> List[dict]:
        if not account:
            return []
        url = config("DW_BALANCE_URL")
        response = await self.execute_get_with_auth(url=url, account=account, query_params={})

        return response

    async def execute_get_with_auth(
        self, url, account: str, query_params: dict
    ) -> List[dict]:
        await self._do_authentication()
        session = await self._get_session()
        headers = {
            "Accept": "application/json",
            "dw-client-app-key": config("DW_APP_KEY"),
            "dw-auth-token": self.token,
        }
        url_formatted = url.format(account)

        async with session.get(url=url_formatted, params=query_params, headers=headers) as response:
            not_ok_response = response.status != 200
            if not_ok_response:
                print(
                    f"DWTransport::execute_get_with_auth::Erros to get data from dw {response}"
                )

            response = await self._response_body_in_json_and_account_id(response=response, base_url=url_formatted)

        return response

    async def _do_authentication(self):
        if not self.expire_at or self.expire_at < datetime.now():
            session = await self._get_session()
            payload = {
                "username": config("DW_USER"),
                "password": config("DW_PASSWORD"),
                "appTypeID": 4,
            }
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "dw-client-app-key": config("DW_APP_KEY"),
            }
            try:
                async with session.post(
                    config("DW_AUTHENTICATION_URL"), json=payload, headers=headers
                ) as response:
                    body = await response.text()
                    dict_body = json.loads(body)
                    self.token = dict_body["authToken"]
                    self.expire_at = datetime.fromisoformat(dict_body["expiresAt"][:-1])
            except Exception as exception:
                print(
                    f"DWTransport::get_balances::Error to authenticate:  {exception}"
                )

    @classmethod
    async def _get_session(cls) -> ClientSession:
        if cls.session is None:
            cls.session = ClientSession()
        return cls.session

    @staticmethod
    async def _consolidate_balances(responses_bodies: List[dict]):
        balances = list()
        for responses_body in responses_bodies:
            try:
                balances.append(
                    {
                        "account": responses_body["account"],
                        "value": float(
                            responses_body["dict_body"]["cash"]["cashAvailableForTrade"]
                        ),
                    }
                )
            except Exception as exception:
                print(
                    f"DWTransport::_consolidate_balances::Error to fetch transaction {responses_body}:  {exception}",
                )
        return balances

    @staticmethod
    async def _response_body_in_json_and_account_id(
        response: ClientResponse, base_url: str
    ) -> List[dict]:
        bodies = list()
        body = await response.text()
        dict_body = json.loads(body)
        bodies.append({"dict_body": dict_body})
        return bodies
