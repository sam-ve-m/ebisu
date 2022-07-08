import asyncio
import json
from typing import List

from etria_logger import Gladsheim
from mepho import DWApiTransport

from src.domain.balance.us.model import Balance
from src.domain.exception import FailToGetDataFromTransportLayer
from src.domain.positions.model import Position
from src.infrastructures.env_config import config


class DwBalanceTransport:
    __transport = DWApiTransport

    @classmethod
    async def get_balances(cls, accounts: List[str]) -> List[Balance]:
        url = config("DW_BALANCE_URL")
        balances = await cls.__execute_get(url=url, accounts=accounts, query_params={})
        return balances

    @classmethod
    async def __execute_get(
        cls, url, accounts: List[str], query_params: dict
    ) -> List[Balance]:
        future_request = list()
        for account in accounts:
            url_formatted = url.format(account)
            future_request.append(
                cls.__transport.execute_get(
                    url=url_formatted, query_params=query_params
                )
            )
        responses = await asyncio.gather(*future_request)
        not_ok_responses = list(filter(lambda x: x.status != 200, responses))
        ok_responses = list(filter(lambda x: x.status == 200, responses))

        if not_ok_responses:
            Gladsheim.error(
                message=f"DwBalanceTransport::__execute_get::Error error getting balance from dw", responses_with_error=not_ok_responses
            )
            raise FailToGetDataFromTransportLayer

        all_balances = []
        for response in ok_responses:
            body_text = await response.text()
            body_json = json.loads(body_text)

            try:
                balance_dw = body_json['cash']
                balance = cls.__consolidate_balance(balance_dw)
                all_balances.append(balance)

            except Exception as error:
                dw_error = body_json.get("errorCode")
                dw_message = body_json.get("message")
                Gladsheim.error(
                    error=error,
                    message=f"DwBalanceTransport::__execute_get::Error error getting balance from dw",
                    dw_error=dw_error,
                    dw_message=dw_message
                )
                raise FailToGetDataFromTransportLayer

        return all_balances

    @staticmethod
    def __consolidate_balance(dw_balace: dict) -> Balance:
        balance = Balance(
                available_for_trade=float(dw_balace["cashAvailableForTrade"]),
                available_for_withdraw=float(dw_balace["cashAvailableForWithdrawal"]),
                cash_balance=float(dw_balace["cashBalance"])
            )

        return balance
