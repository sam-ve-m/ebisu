# INTERNAL LIBS
from datetime import datetime


class ExchangeOperationsModel:
    def __init__(self,
                 unique_id: str,
                 name: str,
                 cpf: str,
                 value: float,
                 cash_conversion: float,
                 spread,
                 tax: float,
                 convert_value: float,
                 due_date: datetime,
                 ):

        self.unique_id = unique_id
        self.name = name
        self.cpf = cpf
        self.date = datetime.utcnow()
        self.value = value
        self.cash_conversion = cash_conversion
        self.spread = spread
        self.tax = tax
        self.convert_value = convert_value
        self.due_date = due_date

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
