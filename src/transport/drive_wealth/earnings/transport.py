# STANDARD IMPORTS
import json
from typing import List
from datetime import datetime, timedelta

# EXTERNAL IMPORTS
from mepho import DWApiTransport

# PROJECT IMPORTS
from src.domain.date_formatters.region.date_time.model import RegionStringDateTime
from src.domain.date_formatters.region.enum.date_format.enum import RegionDateFormat
from src.domain.date_formatters.region.timestamp.model import RegionTimeStamp
from src.domain.earning.base.model.earning.model import Earning
from src.domain.statement.us.request.model import TransactionRequest
from src.infrastructures.env_config import config
from src.transport.drive_wealth.statement.transport import DwStatementTransport


class DwEarningsTransport:

    transaction_url = config("DW_GET_ALL_TRANSACTIONS_URL")
    balance_url = config("DW_BALANCE_URL")

    @staticmethod
    def __build_earning_model(transaction: dict) -> Earning:
        earning_model = Earning(
            symbol=transaction.get("instrument", {}).get("symbol", {}),
            name=transaction.get("instrument", {}).get("name", {}),
            amount_per_share=transaction.get("dividend", {}).get("amountPerShare", {}),
            type=transaction.get("dividend", {}).get("type", {}),
            tax_code=transaction.get("dividend", {}).get("taxCode", {}),
            date=RegionStringDateTime(
                date=transaction.get("tranWhen", {}),
                region_date_format=RegionDateFormat.US_DATE_FORMAT
            )
        )

        return earning_model

    @staticmethod
    async def get_us_transaction_earnings(
            transaction_request: TransactionRequest
    ) -> List[Earning]:
        transactions = await DwEarningsTransport.__get_transactions(
            transaction_request=transaction_request
        )

        earnings_model = [
            DwEarningsTransport.__build_earning_model(transaction=transaction)
            for transaction in transactions]
        return earnings_model

    @staticmethod
    async def __get_transactions(
            transaction_request: TransactionRequest
    ) -> dict:
        query_params = transaction_request.get_query_params()
        account = transaction_request.get_account()
        url_formatted = DwStatementTransport.transaction_url.format(account)

        response = await DWApiTransport.execute_get(
            url=url_formatted,
            query_params=query_params
        )

        body = await response.text()
        transactions = json.loads(body)
        return transactions

    @staticmethod
    def __get_yesterday_date() -> RegionTimeStamp:
        yesterday_date = datetime.now() - timedelta(1)
        raw_yesterday_date = int(yesterday_date.timestamp() * 1000)
        converted_date = RegionTimeStamp(timestamp=raw_yesterday_date, region_date_format=RegionDateFormat.US_DATE_FORMAT)
        return converted_date
