# Ebisu
from src.domain.date_formatters.region.date_time.model import RegionStringDateTime
from src.domain.date_formatters.region.enum.date_format.enum import RegionDateFormat
from src.domain.date_formatters.region.enum.utc_offset.enum import ExchangeUtcOffset
from src.domain.enums.forex_exchange import CurrencyOptions, NatureOperation

# Standards
from datetime import datetime

# Third party
from pydantic import BaseModel


class CustomerExchangeResponseModel(BaseModel):
    exchange_account_id: int
    operation_nature_code: NatureOperation
    base_currency_symbol: CurrencyOptions
    quote_currency_symbol: CurrencyOptions
    quantity_currency_traded: float
    currency_quote_price: float
    tax_value: float
    gross_value: float
    iof_percentage: float
    iof_value: float
    net_value: float
    vet: float
    quote_date: int
    expiration_date: int
    payment_date: int
    spread_percentage: float
    commercial_tax: float
    proposal_token: str

    @classmethod
    async def get_customer_exchange_model(cls, exchange_simulation_proposal_data: dict):
        values = exchange_simulation_proposal_data.get("valores", {})
        base_currency_symbol = values.get("simboloMoedaBase")
        commercial_tax = values.get("taxaComercial")
        currency_quote_price = values.get("valorCotacaoCambio")
        exchange_account_id = values.get("codigoCliente")
        expiration_date = cls.__convert_date_to_time_stamp(date=values.get("dataValidade"))
        gross_value = values.get("valorBruto")
        iof_percentage = values.get("percentualIOF")
        iof_value = values.get("valorIOF")
        net_value = values.get("valorLiquido")
        operation_nature_code = values.get("codigoNaturezaOperacao")
        payment_date = cls.__convert_date_to_time_stamp(date=values.get("dataPagamento"))
        proposal_token = exchange_simulation_proposal_data.get("token")
        quote_currency_symbol = values.get("simboloMoedaCotacao")
        quote_date = cls.__convert_date_to_time_stamp(date=values.get("dataCotacao"))
        quantity_currency_traded = values.get("quantidadeMoedaNegociada")
        spread_percentage = values.get("percentualSpread")
        tax_value = values.get("valorTarifa")
        vet = values.get("vet")

        exchange_data_to_validate = {
            "base_currency_symbol": base_currency_symbol,
            "commercial_tax": commercial_tax,
            "currency_quote_price": currency_quote_price,
            "exchange_account_id": exchange_account_id,
            "expiration_date": expiration_date,
            "gross_value": gross_value,
            "iof_percentage": iof_percentage,
            "iof_value": iof_value,
            "net_value": net_value,
            "operation_nature_code": operation_nature_code,
            "payment_date": payment_date,
            "proposal_token": proposal_token,
            "quote_currency_symbol": quote_currency_symbol,
            "quote_date": quote_date,
            "quantity_currency_traded": quantity_currency_traded,
            "spread_percentage": spread_percentage,
            "tax_value": tax_value,
            "vet": vet
        }

        return cls(**exchange_data_to_validate)

    @staticmethod
    async def __convert_date_to_time_stamp(date: datetime):
        converted_date = RegionStringDateTime(
            region_date_format=RegionDateFormat.BR_DATE_ISO_FORMAT,
            date=date,
            utc_offset=ExchangeUtcOffset.BR_UTC_OFFSET
        )
        return converted_date.get_date_in_time_stamp_with_timezone_replace()
