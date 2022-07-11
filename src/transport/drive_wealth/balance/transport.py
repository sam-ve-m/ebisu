import json

from etria_logger import Gladsheim
from mepho import DWApiTransport

from src.domain.balance.us.model import Balance
from src.infrastructures.env_config import config
from src.transport.drive_wealth.base.transport import DwBaseTransport


class DwBalanceTransport(DwBaseTransport):
    __balance_url = config("DW_BALANCE_URL")

    @staticmethod
    async def get_balance(account: str) -> Balance:
        try:

            url_formatted = DwBalanceTransport.__balance_url.format(account)
            response = await DWApiTransport.execute_get(url=url_formatted, query_params={})

            DwBalanceTransport._handle_http_error_from_drive_wealth_request(
                request=url_formatted,
                response=response
            )

            body = await response.text()
            response = json.loads(body)

            DwBalanceTransport._handle_dw_error_status_from_response(
                request=url_formatted,
                response=response
            )

            cash = response["cash"]
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
