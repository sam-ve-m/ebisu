# STANDARD IMPORTS
from typing import List, Union
from pydantic import BaseModel

# PROJECT IMPORTS
from src.domain.statement.base.response.model import TransactionResponse
from src.domain.statement.base.model.transaction.model import Transaction


class StatementResponse(BaseModel):
    transactions: List[TransactionResponse]
    offset: Union[int, None]


class StatementModelToResponse:

    @staticmethod
    def __extract_next_offset_from_transactions(transactions: List[Transaction]):
        offset = None

        has_transactions = bool(transactions)
        if has_transactions:
            last_transaction = transactions[-1]
            transaction_response = last_transaction.__repr__()
            offset = transaction_response.get("date")

        return offset

    @staticmethod
    def statement_response(transactions: List[Transaction]):
        transactions_response = [TransactionResponse(**transaction.__repr__()) for transaction in transactions]
        offset = StatementModelToResponse.__extract_next_offset_from_transactions(transactions)

        statement_dict = {
            "transactions": transactions_response,
            "offset": offset
        }

        statement_response = StatementResponse(**statement_dict)

        return statement_response
