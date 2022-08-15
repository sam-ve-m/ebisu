from src.domain.statement.base.model.transaction.model import Transaction


class UsTransaction(Transaction):
    def __repr__(self):
        transaction = {
            "date": self.date.get_date_in_timestamp_with_timezone_offset(),
            "description": self.description,
            "value": self.value,
        }

        return transaction
