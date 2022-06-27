# STANDARD LIBS
from datetime import datetime, timedelta
from typing import List

# PROJECT IMPORTS
from src.domain.statement.us.request.model import TransactionRequest, QueryParams
from src.transport.drive_wealth.earnings.transport import DwEarningsTransport
from src.transport.drive_wealth.statement.transport import DwStatementTransport
from tests.src.services.earnings_from_client.stub_earnings import dw_earnings_example


class GetUsEarningsDetails:
    dw = DwStatementTransport()

    @staticmethod
    def normalize_earnings_us(client_earnings: dict) -> List[dict]:
        earnings_us = []
        # TODO - as long as DW doesn't show the net price of dividends, this needs to be implemented later
        for transaction in client_earnings.get("dict_body"):
            earnings_us.append(
                {
                    "symbol": transaction.get("instrument", {}).get("symbol", {}),
                    "name": transaction.get("instrument", {}).get("name", {}),
                    "amount per share": transaction.get("dividend", {}).get("amountPerShare", {}),
                    "type": transaction.get("dividend", {}).get("type", {}),
                    "tax code": transaction.get("dividend", {}).get("taxCode", {}),
                    "transaction date": transaction.get("tranWhen", {}),
                }
            )

        if not earnings_us[0].get("amount per share"):
            return []

        return earnings_us

    @staticmethod
    def get_paid_and_payable_earnings(earnings_response: list):

        for earnings in earnings_response:
            transaction_date = earnings.get("transaction date")
            convert_to_date_time = datetime.strptime(transaction_date, '%Y-%m-%dT%H:%M:%S.%fZ')
            earnings.update({"transaction date": convert_to_date_time})

        yesterday_date = datetime.now() - timedelta(1)

        paid_earnings_client = \
            [key for key in earnings_response if key.get("transaction date") < yesterday_date]
        payable_earnings_client = \
            [key for key in earnings_response if key.get("transaction date") > yesterday_date]

        return paid_earnings_client, payable_earnings_client

    @staticmethod
    async def get_dw_us_earnings(
            dw_account: str, offset, limit: int, start_date, end_date
    ):

        transaction_request = TransactionRequest(
            account=dw_account,
            query_params=QueryParams(from_date=start_date,
                                     to_date=end_date,
                                     offset=offset,
                                     limit=limit
                                     ))

        raw_earnings = await DwEarningsTransport.get_earnings(
            transaction_request=transaction_request
        )

        paid_earnings_client, payable_earnings_client = GetUsEarningsDetails.get_paid_and_payable_earnings(
            earnings_response=raw_earnings
        )

        earnings_normalized_response = {
            "paid_earnings_client": paid_earnings_client,
            "payable_earnings_client": payable_earnings_client
        }

        return earnings_normalized_response
