# STANDARD IMPORTS
from typing import List
from pydantic import BaseModel

# PROJECT IMPORTS
from src.domain.earning.base.response.model import EarningsTransactionResponse
from src.domain.statement.base.model.transaction.model import Transaction


class EarningsRecordResponse(BaseModel):
    transactions: List[EarningsTransactionResponse]


class EarningsModelToResponse:

    @staticmethod
    def statement_response(transactions: List[Transaction]):
        earnings_transactions_response = [
            EarningsTransactionResponse(**transaction.__repr__()) for transaction in transactions]

        earnings_dict = {
            "earnings_transactions": earnings_transactions_response,
        }

        earnings_response = EarningsRecordResponse(**earnings_dict)

        return earnings_response
