# STANDARD IMPORTS
from datetime import datetime, timedelta
from typing import List
from pydantic import BaseModel

# PROJECT IMPORTS
from src.domain.earning.base.model.earning.model import Earning
from src.domain.earning.base.response.model import EarningsTransactionResponse


class EarningsRecordResponse(BaseModel):
    paid: List[EarningsTransactionResponse]
    payable: List[EarningsTransactionResponse]


class EarningsModelToResponse:

    @staticmethod
    def get_yesterday_date_in_timestamp():
        today = datetime.utcnow()
        yesterday = today - timedelta(days=1)
        yesterday_in_timestamp = int(datetime.timestamp(yesterday) * 1000)
        return yesterday_in_timestamp

    @staticmethod
    def earnings_response(
            earnings_transactions: List[Earning]):

        yesterday_date = EarningsModelToResponse.get_yesterday_date_in_timestamp()

        paid = [
            EarningsTransactionResponse(
                **earning_paid_transaction.__repr__())
            for earning_paid_transaction in earnings_transactions
            if earning_paid_transaction.date.get_date_in_time_stamp() <= yesterday_date
        ]
        payable = [
            EarningsTransactionResponse(
                **earning_payable_transaction.__repr__())
            for earning_payable_transaction in earnings_transactions
            if earning_payable_transaction.date.get_date_in_time_stamp() > yesterday_date
        ]

        earnings_dict = {
            "paid": paid,
            "payable": payable
        }

        earnings_response = EarningsRecordResponse(**earnings_dict)

        return earnings_response
