import json

from etria_logger import Gladsheim
from mepho import DWApiTransport

from src.domain.balance.us.model import Balance
from src.infrastructures.env_config import config
from src.transport.drive_wealth.base.transport import DwBaseTransport


class DwBalanceTransport(DwBaseTransport):

    __balance_url = config("DW_BALANCE_URL")
    __transport = DWApiTransport

    @classmethod
    async def get_balance(cls, account: str) -> Balance:
        try:
            url_formatted = cls.__balance_url.format(account)
            response = await cls.__transport.execute_get(url=url_formatted, query_params={})

            body = await response.text()
            json_balance = json.loads(body)

            cls._handle_dw_error_status_from_response(
                request=url_formatted,
                response=json_balance
            )

            cls._handle_http_error_from_drive_wealth_request(
                request=url_formatted,
                response=response
            )

            cash = json_balance["cash"]
            balance = Balance(
                available_for_trade=cash.get("cashAvailableForTrade", 0),
                available_for_withdraw=cash.get("cashAvailableForWithdrawal", 0),
                cash_balance=cash.get("cashBalance", 0)
            )

            return balance

        except Exception as err:

            Gladsheim.error(
                message=f"DwBalanceTransport::get_balances::Error when get balance from drive wealth",
                error=err,
            )
            raise err
