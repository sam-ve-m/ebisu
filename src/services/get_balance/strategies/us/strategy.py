from typing import List

from etria_logger import Gladsheim

from src.infrastructures.env_config import config
from src.repositories.drive_wealth.repository import DWRepository


class GetUsBalance(DWRepository):
    @classmethod
    async def get_balances(cls, accounts: List[str]) -> List[dict]:
        if not accounts:
            return []
        url = config("DW_BALANCE_URL")
        responses = await cls._execute_get(url=url, accounts=accounts, query_params={})
        bodies = await cls._response_body_in_json_and_account_id(
            responses=responses, base_url=url
        )
        balances = await cls.__consolidate_balances(responses_bodies=bodies)
        return balances

    @staticmethod
    async def __consolidate_balances(responses_bodies: List[dict]) -> List[dict]:
        balances = list()
        for responses_body in responses_bodies:
            try:
                balances.append(
                    {
                        "account": responses_body["account"],
                        "available_for_trade": float(
                            responses_body["dict_body"]["cash"]["cashAvailableForTrade"]
                        ),
                        "available_for_withdraw": float(
                            responses_body["dict_body"]["cash"][
                                "cashAvailableForWithdrawal"
                            ]
                        ),
                        "cash_balance": float(
                            responses_body["dict_body"]["cash"]["cashBalance"]
                        )
                    }
                )
            except Exception as exception:
                Gladsheim.error(
                    message=f"GetUsBalance::__consolidate_balances::Error to fetch transaction {responses_body}:  {exception}",
                    error=exception,
                )
        return balances

    @classmethod
    async def get_balance(cls, dw_account: str):
        """
        Returns the sum of the absolute value of all customer balances.

        WARNING: The function does not return the customer's balance and is only used to check if the account balance is empty.
        """
        user_balances = await cls.get_balances([dw_account])
        user_balances = user_balances[0]
        trade_balance = abs(user_balances["available_for_trade"])
        withdraw_balance = abs(user_balances["available_for_withdraw"])
        cash_balance = abs(user_balances["cash_balance"])
        balances_sum = trade_balance + withdraw_balance + cash_balance

        account_balance = {
            "balance": balances_sum
        }
        return account_balance
