# Standards
from typing import Optional, Any, List

# Third party
from pydantic import BaseModel


class ExecutionResponseModel(BaseModel):
    unique_id: str
    forex_account: int
    exchange_operation_code: int
    exchange_status_code: int
    exchange_status_name: str
    nature_operation_code: int
    nature_name: Optional[str]
    transaction_type: str
    operation_mode: str
    agency_number: Optional[int]
    account_number: Optional[int]
    account_digit: Optional[int]
    bank_number: Optional[str]
    bank_name: Optional[str]
    label: Optional[Any]
    overseas_banker: Optional[Any]
    payment_currency_bacen_code: int
    payment_currency_symbol: str
    traded_currency_bacen_code: int
    traded_currency_symbol: str
    quantity_traded: Optional[Any]
    payment_amount: Optional[float]
    total_value: float
    documents: Optional[List]
    IOF_percentage: float
    tariff: float
    control_code: str
    control_message: str
    control_token: Optional[str]
    control_datetime: str

    @classmethod
    def get_model(cls, execution_response: dict, unique_id: str):
        exchange_operation = execution_response.get("operacaoCambio", {})
        execution_response_to_validate = {
            "unique_id": unique_id,
            "forex_account": execution_response.get("cliente", {}).get("codigo"),
            "exchange_operation_code": exchange_operation.get("codigo"),
            "exchange_status_code": exchange_operation.get("status", {}).get("codigo"),
            "exchange_status_name": exchange_operation.get("status", {}).get("nome"),
            "nature_operation_code": exchange_operation.get("naturezaOperacao", {}).get(
                "codigo"
            ),
            "nature_name": exchange_operation.get("naturezaOperacao", {}).get("nome"),
            "transaction_type": exchange_operation.get("naturezaOperacao", {}).get(
                "tipoTransacao"
            ),
            "operation_mode": exchange_operation.get("naturezaOperacao", {}).get(
                "modoOperacao"
            ),
            "agency_number": exchange_operation.get("dadosLiquidacao", {}).get(
                "numeroAgencia") if exchange_operation.get("dadosLiquidacao") else None,
            "account_number": exchange_operation.get("dadosLiquidacao", {}).get(
                "numeroConta") if exchange_operation.get("dadosLiquidacao") else None,
            "account_digit": exchange_operation.get("dadosLiquidacao", {}).get(
                "digitoConta") if exchange_operation.get("dadosLiquidacao") else None,
            "bank_number": exchange_operation.get("dadosLiquidacao").get(
                "numeroBanco") if exchange_operation.get("dadosLiquidacao") else None,
            "bank_name": exchange_operation.get("dadosLiquidacao", {}).get("nomeBanco")
            if exchange_operation.get("dadosLiquidacao") else None,
            "label": exchange_operation.get("dadosLiquidacao", {}).get("rotulo")
            if exchange_operation.get("dadosLiquidacao") else None,
            "overseas_banker": exchange_operation.get("dadosBanqueiroExterior"),
            "payment_currency_bacen_code": exchange_operation.get(
                "moedaPagamento", {}
            ).get("codigoBACEN"),
            "payment_currency_symbol": exchange_operation.get("moedaPagamento", {}).get(
                "simbolo"
            ),
            "traded_currency_bacen_code": exchange_operation.get(
                "moedaNegociada", {}
            ).get("codigoBACEN"),
            "traded_currency_symbol": exchange_operation.get("moedaNegociada", {}).get(
                "simbolo"
            ),
            "quantity_traded": exchange_operation.get("quantidadeNegociada"),
            "payment_amount": exchange_operation.get("quantidadePagamento"),
            "total_value": exchange_operation.get("valorTotal"),
            "documents": exchange_operation.get("documentos"),
            "IOF_percentage": exchange_operation.get("percentualIOF"),
            "tariff": exchange_operation.get("tarifa"),
            "control_code": execution_response.get("controle", {}).get("codigo"),
            "control_message": execution_response.get("controle", {}).get("mensagem"),
            "control_token": execution_response.get("controle", {}).get("token"),
            "control_datetime": execution_response.get("controle", {}).get(
                "dataHoraServidor"
            ),
        }
        return cls(**execution_response_to_validate)
