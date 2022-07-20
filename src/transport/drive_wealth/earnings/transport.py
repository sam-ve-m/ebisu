# STANDARD IMPORTS
import json
from typing import List

# EXTERNAL IMPORTS
from mepho import DWApiTransport

# PROJECT IMPORTS
from src.domain.date_formatters.region.date_time.model import RegionStringDateTime
from src.domain.date_formatters.region.enum.date_format.enum import RegionDateFormat
from src.domain.date_formatters.region.enum.utc_offset.enum import ExchangeUtcOffset
from src.domain.earning.us.model import Earning
from src.domain.exception.model import FailToGetDataFromTransportLayer
from src.domain.statement.us.request.model import TransactionRequest
from src.infrastructures.env_config import config


class DwEarningsTransport:

    transaction_url = config("DW_GET_ALL_TRANSACTIONS_URL")
    balance_url = config("DW_BALANCE_URL")

    @staticmethod
    def __build_earning_model(earning_transaction: dict) -> Earning:
        earning_model = Earning(
            symbol=earning_transaction.get("instrument", {}).get("symbol"),
            description=earning_transaction.get("instrument", {}).get("name"),
            amount_per_share=earning_transaction.get("dividend", {}).get(
                "amountPerShare"
            ),
            date=RegionStringDateTime(
                date=earning_transaction.get("tranWhen"),
                utc_offset=ExchangeUtcOffset.US_UTC_OFFSET,
                region_date_format=RegionDateFormat.US_DATE_FORMAT,
            ),
            amount=earning_transaction.get("accountAmount"),
        )

        return earning_model

    @staticmethod
    async def get_us_transaction_earnings(
        transaction_request: TransactionRequest,
    ) -> List[Earning]:
        earnings_transactions = await DwEarningsTransport.__get_transactions(
            transaction_request=transaction_request
        )
        earnings_model = [
            DwEarningsTransport.__build_earning_model(
                earning_transaction=earning_transaction
            )
            for earning_transaction in earnings_transactions
            if earning_transaction.get("dividend")
        ]

        return earnings_model

    @staticmethod
    async def __get_transactions(transaction_request: TransactionRequest) -> dict:
        query_params = transaction_request.get_query_params()
        account = transaction_request.get_account()
        url_formatted = DwEarningsTransport.transaction_url.format(account)

        response = await DWApiTransport.execute_get(
            url=url_formatted, query_params=query_params
        )
        if response.status == 200:
            body = await response.text()
            transactions = json.loads(body)
            return transactions
        raise FailToGetDataFromTransportLayer()
