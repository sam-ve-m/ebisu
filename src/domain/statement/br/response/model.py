from typing import List

from pydantic import BaseModel

from src.domain.statement.base.response.model import TransactionResponse
from src.domain.statement.base.model.transaction.model import Transaction


class StatementResponse(BaseModel):
    transactions: List[TransactionResponse]


class StatementModelToResponse:
    @staticmethod
    def statement_response(transactions: List[Transaction]):
        transactions_response = [
            TransactionResponse(**transaction.__repr__())
            for transaction in transactions
        ]

        statement_dict = {"transactions": transactions_response}

        statement_response = StatementResponse(**statement_dict)

        return statement_response
