# PROJECT IMPORTS
from src.domain.statement.base.model.transaction.model import Transaction


class BrTransaction(Transaction):

    def __repr__(self):
        transaction = {
            "date": self.date.get_date_in_time_stamp_with_timezone_replace(),
            "description": self.description,
            "value": self.value,
        }

        return transaction
