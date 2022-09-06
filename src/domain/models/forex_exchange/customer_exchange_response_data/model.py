# Ebisu
from src.domain.enums.forex_exchange import CurrencyOptions, NatureOperation

# Standards
from datetime import datetime
from typing import Union

# Third party
from pydantic import BaseModel


class CustomerExchangeResponseModel(BaseModel):
    exchange_account_id: int
    operation_nature_code: NatureOperation
    base_currency_symbol: CurrencyOptions
    quote_currency_symbol: CurrencyOptions
    quantity_currency_traded: Union[float, int]
    currency_quote_price: Union[float, int]
    tax_value: Union[float, int]
    gross_value: Union[float, int]
    iof_percentage: Union[float, int]
    iof_value: Union[float, int]
    net_value: Union[float, int]
    vet: Union[float, int]
    quote_date: datetime
    expiration_date: datetime
    payment_date: datetime
    spread_percentage: Union[float, int]
    commercial_tax: Union[float, int]
    token: str

    @classmethod
    def get_customer_exchange_response_model(cls, exchange_simulation_proposal_data: dict):
        values = exchange_simulation_proposal_data.get("valores", {})
        exchange_template_to_us = {
            "exchange_account_id": values.get("codigoCliente"),
            "operation_nature_code": values.get("codigoNaturezaOperacao"),
            "base_currency_symbol": values.get("simboloMoedaBase"),
            "quote_currency_symbol": values.get("simboloMoedaCotacao"),
            "quantity_currency_traded": values.get(
                "quantidadeMoedaNegociada"),
            "currency_quote_price": values.get("valorCotacaoCambio"),
            "tax_value": values.get("valorTarifa"),
            "gross_value": values.get("valorBruto"),
            "iof_percentage": values.get("percentualIOF"),
            "iof_value": values.get("valorIOF"),
            "net_value": values.get("valorLiquido"),
            "vet": values.get("vet"),
            "quote_date": values.get("dataCotacao"),
            "expiration_date": values.get("dataValidade"),
            "payment_date": values.get("dataPagamento"),
            "spread_percentage": values.get("percentualSpread"),
            "commercial_tax": values.get("taxaComercial"),
            "token": exchange_simulation_proposal_data.get("token"),
        }
        return cls(**exchange_template_to_us)
