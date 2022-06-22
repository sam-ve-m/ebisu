# INTERNAL LIBS
from datetime import datetime


class ExchangeOperationsModel:
    def __init__(self, exchange_operations_dto: dict):

        self.unique_id = exchange_operations_dto.get("unique_id")
        self.name = exchange_operations_dto.get("name")
        self.cpf = exchange_operations_dto.get("cpf")
        self.date = datetime.utcnow()
        self.value = exchange_operations_dto.get("value")
        self.cash_conversion = exchange_operations_dto.get("cash_conversion")
        self.spread = exchange_operations_dto.get("spread")
        self.tax = exchange_operations_dto.get("tax")
        self.convert_value = exchange_operations_dto.get("convert_value")
        self.due_date = exchange_operations_dto.get("due_date")

    def get_exchange_operations_template(self) -> dict:

        exchange_operations_template = {
                "unique_id": self.unique_id,
                "name": self.name,
                "cpf": self.cpf,
                "contract": "101010",
                "ref_int": 123,
                "week":20,
                "tp": "C",
                "du_brl": 4.5,
                "dc_usd": 5.5,
                "ajuste_brl": 1.4,
                "ajuste_usd": 1.0,
                "spot_client": 12344.45,
                "zeramento": 5.6,
                "cdi": "10.65%",
                "linha": "0.15%",
                "pnl": 103.87,
                "value": self.value,
                "cash_conversion": self.cash_conversion,
                "spread": self.spread,
                "tax": self.tax,
                "convert_value": self.convert_value,
                "due_date": self.due_date
            }

        return exchange_operations_template
