# STANDARD IMPORTS
from typing import List
from pydantic import BaseModel

# PROJECT IMPORTS
from src.domain.earning.br.model import EarningBr
from src.domain.earning.base.response.model import EarningsTransactionBrResponse


class EarningsRecordResponse(BaseModel):
    paid: List[EarningsTransactionBrResponse]
    payable: List[EarningsTransactionBrResponse]
    record_date: List[EarningsTransactionBrResponse]
    total_paid: float


class BrEarningsModelToResponse:
    @staticmethod
    def earnings_response(
        payable_transactions: List[EarningBr],
        paid_transactions: List[EarningBr],
        record_transactions: List[EarningBr],
        total_paid_transactions: float,
    ):

        total_paid = round(total_paid_transactions, 2)

        payable = [
            EarningsTransactionBrResponse(**earning_payable_transaction.__repr__())
            for earning_payable_transaction in payable_transactions
        ]

        paid = [
            EarningsTransactionBrResponse(**earning_paid_transaction.__repr__())
            for earning_paid_transaction in paid_transactions
        ]

        record_date = [
            EarningsTransactionBrResponse(**earning_paid_transaction.__repr__())
            for earning_paid_transaction in record_transactions
        ]

        earnings_dict = {
            "total_paid": total_paid,
            "paid": paid,
            "payable": payable,
            "record_date": record_date,
        }

        earnings_response = EarningsRecordResponse(**earnings_dict)

        return earnings_response
