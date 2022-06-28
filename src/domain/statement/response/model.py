from typing import List
from pydantic import BaseModel

from src.domain.statement.model.balance.model import Balance
from src.domain.statement.model.transaction.model import Transaction


class BalanceResponse(BaseModel):
    value: float


class TransactionResponse(BaseModel):
    date: int
    description: str
    value: float


class StatementResponse(BaseModel):
    balance: BalanceResponse
    transactions: List[TransactionResponse]


class Paginated(BaseModel):
    statement: StatementResponse
    next_date: int


class StatementModelToResponse:
    @staticmethod
    def statement_response(balance: Balance, transactions: List[Transaction]):
        balance_response = BalanceResponse(**balance.__repr__())
        transactions_response = [
            TransactionResponse(**transaction.__repr__())
            for transaction in transactions
        ]

        statement_dict = {
            "balance": balance_response,
            "transactions": transactions_response,
        }

        statement_response = StatementResponse(**statement_dict)

        return statement_response
