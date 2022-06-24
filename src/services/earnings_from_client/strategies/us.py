# STANDARD LIBS
from datetime import datetime, timedelta
from typing import List
import pytz

# PROJECT IMPORTS
from src.domain.statement.us.request.model import TransactionRequest, QueryParams
from src.services.earnings_from_client.strategies.earnings_client_example import dw_earnings_example
from src.transport.drive_wealth.statement.transport import DwStatementTransport


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

        raw_earnings = await GetUsEarningsDetails.dw.get_transactions(
            transaction_request=transaction_request
        )

        earnings_response = GetUsEarningsDetails.normalize_earnings_us(*dw_earnings_example)

        yesterday_date = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')  # 2022-06-23

        paid_earnings_client = {key for key in earnings_response if key.get("transaction date") < yesterday_date}
        payable_earnings_client = {key for key in earnings_response if key.get("transaction date") > yesterday_date}

        if not earnings_response:
            empty_earnings = {
                "paid_earnings_client": [],
                "payable_earnings_client": []
            }
            return empty_earnings

        earnings_normalized_response = {
            "paid_earnings_client": paid_earnings_client,
            "payable_earnings_client": payable_earnings_client
        }

        return earnings_normalized_response
