from typing import TypedDict, Optional


class ExchangeOperationsDto(TypedDict):
    name: Optional[str]
    cpf: Optional[str]
    unique_id: Optional[str]
    value: Optional[float]
    cash_conversion: Optional[str]
    spread: Optional[str]
    tax: Optional[float]
    convert_value: Optional[float]
    due_date: Optional[str]


class ExchangeOperationsDtoBuilder:
    @staticmethod
    def build(jwt_data: dict, resume: dict, name: str, cpf: str) -> dict:
        user = jwt_data.get("user")

        exchange_operations_dto: ExchangeOperationsDto = {
            "name": name,
            "cpf": cpf,
            "unique_id": user.get("unique_id"),
            "value": resume.get("value"),
            "cash_conversion": resume.get("cash_conversion"),
            "spread": resume.get("spread"),
            "tax": resume.get("tax"),
            "convert_value": resume.get("convert_value"),
            "due_date": resume.get("due_date"),
        }
        return exchange_operations_dto
