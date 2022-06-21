# Standards
import json
from typing import List

# Third part
from aiohttp import ClientResponse

from mepho import DWApiTransport

from src.domain.statement.us.request.model import TransactionRequest
from src.infrastructures.env_config import config


class DwStatementTransport:
    session = None

    @staticmethod
    async def get_transactions(
        transaction_request: TransactionRequest
    ) -> List[dict]:
        url = config("DW_GET_ALL_TRANSACTIONS_URL")

        query_params = transaction_request.get_query_params()
        account = transaction_request.get_account()
        url_formatted = url.format(account)

        response = await DWApiTransport.execute_get(
            url=url_formatted,
            query_params=query_params
        )
        response = await DwStatementTransport.__response_body_in_json_and_account_id(response=response)
        return response

    @staticmethod
    async def get_balances(account: str) -> List[dict]:
        if not account:
            return {}
        url = config("DW_BALANCE_URL")

        url_formatted = url.format(account)
        response = await DWApiTransport.execute_get(url=url_formatted, query_params={})
        response = await DwStatementTransport.__response_body_in_json_and_account_id(response=response)
        return response

    @staticmethod
    async def __response_body_in_json_and_account_id(
        response: ClientResponse,
    ) -> List[dict]:
        bodies = list()
        body = await response.text()
        dict_body = json.loads(body)
        bodies.append({"dict_body": dict_body})
        return bodies
