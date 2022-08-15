# STANDARD IMPORTS
import json
from typing import List

# EXTERNAL IMPORTS
from mepho import DWApiTransport

# PROJECT IMPORTS
from src.domain.date_formatters.region.date_time.model import RegionStringDateTime
from src.domain.date_formatters.region.enum.date_format.enum import RegionDateFormat
from src.domain.date_formatters.region.enum.utc_offset.enum import ExchangeUtcOffset
from src.domain.statement.base.model.transaction.model import Transaction
from src.domain.statement.us.model import UsTransaction
from src.domain.statement.us.request.model import TransactionRequest
from src.infrastructures.env_config import config
from src.transport.drive_wealth.base.transport import DwBaseTransport


class DwStatementTransport(DwBaseTransport):
    transaction_url = config("DW_GET_ALL_TRANSACTIONS_URL")

    @staticmethod
    def __build_transaction_model(transaction: dict) -> Transaction:
        transaction_model = UsTransaction(
            description=transaction.get("comment"),
            value=transaction.get("tranAmount"),
            date=RegionStringDateTime(
                date=transaction.get("tranWhen"),
                utc_offset=ExchangeUtcOffset.US_UTC_OFFSET,
                region_date_format=RegionDateFormat.US_DATE_FORMAT,
            ),
        )

        return transaction_model

    @staticmethod
    async def get_inflow_transactions(
        transaction_request: TransactionRequest,
    ) -> List[Transaction]:
        transactions = await DwStatementTransport.__get_transactions(
            transaction_request=transaction_request
        )

        transactions_model = [
            DwStatementTransport.__build_transaction_model(transaction=transaction)
            for transaction in transactions
            if transaction.get("tranAmount") > 0
        ]

        return transactions_model

    @staticmethod
    async def get_outflow_transactions(
        transaction_request: TransactionRequest,
    ) -> List[Transaction]:
        transactions = await DwStatementTransport.__get_transactions(
            transaction_request=transaction_request
        )

        transactions_model = [
            DwStatementTransport.__build_transaction_model(transaction=transaction)
            for transaction in transactions
            if transaction.get("tranAmount") < 0
        ]

        return transactions_model

    @staticmethod
    async def get_transactions(
        transaction_request: TransactionRequest,
    ) -> List[Transaction]:

        transactions = await DwStatementTransport.__get_transactions(
            transaction_request=transaction_request
        )

        transactions_model = [
            DwStatementTransport.__build_transaction_model(transaction=transaction)
            for transaction in transactions
        ]

        return transactions_model

    @classmethod
    async def __get_transactions(cls, transaction_request: TransactionRequest) -> dict:
        query_params = transaction_request.get_query_params()
        account = transaction_request.get_account()
        url_formatted = DwStatementTransport.transaction_url.format(account)

        response = await DWApiTransport.execute_get(
            url=url_formatted, query_params=query_params
        )

        body = await response.text()
        transactions = json.loads(body)

        cls._handle_dw_error_status_from_response(
            request=url_formatted, response=transactions
        )

        cls._handle_http_error_from_drive_wealth_request(
            request=url_formatted, response=response
        )

        return transactions
