from etria_logger import Gladsheim

from src.transport.drive_wealth.balance.transport import DwBalanceTransport


class GetUsBalance:
    dw_transport = DwBalanceTransport

    @classmethod
    async def get_balance(cls, dw_account: str):
        """
        Returns the sum of the absolute value of all customer balances.

        WARNING: The function does not return the customer's balance and is only used to check if the account balance is empty.
        """
        try:
            user_balance = await cls.dw_transport.get_balances([dw_account])
            user_balance = user_balance[0]
            trade_balance = abs(user_balance.available_for_trade)
            withdraw_balance = abs(user_balance.available_for_withdraw)
            cash_balance = abs(user_balance.cash_balance)
            balances_sum = trade_balance + withdraw_balance + cash_balance

            account_balance = {"balance": balances_sum}

        except Exception as ex:
            Gladsheim.error(
                message=f"GetUsBalance::get_balance::Error to get balance in US",
                dw_account=dw_account,
                error=ex,
            )
            raise ex

        return account_balance
