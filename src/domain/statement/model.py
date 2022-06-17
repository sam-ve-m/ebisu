from typing import List

from pydantic import BaseModel

from src.domain.statement.balance.model import Balance
from src.domain.statement.transaction.model import Transaction


class Statement:

    def __init__(self, balance: Balance, transactions: List[Transaction]):
        self.__transactions = transactions
        self.__balance = balance

    def get_statement_response(self):
        pass

