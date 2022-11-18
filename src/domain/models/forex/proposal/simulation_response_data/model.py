# Ebisu
from src.domain.validators.forex.proposal.simulation.validator import (
    ContentRoute22,
    ContentRoute21,
)

# Standards
from datetime import datetime


class SimulationResponseModel:
    def __init__(
        self,
        content_21_validated: ContentRoute21,
        content_22_validated: ContentRoute22,
        unique_id: str,
    ):
        self.commercial_fee = content_21_validated.taxa.taxaComercial
        self.client_fee = content_21_validated.taxa.valorTotal
        self.base_currency_symbol = content_22_validated.valores.simboloMoedaBase
        self.commercial_fee = content_22_validated.valores.taxaComercial
        self.currency_quote_price = content_22_validated.valores.valorCotacaoCambio
        self.client_id = content_22_validated.valores.codigoCliente
        self.expiration_date = content_22_validated.valores.dataValidade
        self.gross_value = content_22_validated.valores.valorBruto
        self.iof_percentage = content_22_validated.valores.percentualIOF
        self.iof_value = content_22_validated.valores.valorIOF
        self.net_value = content_22_validated.valores.valorLiquido
        self.nature_operation_code = content_22_validated.valores.codigoNaturezaOperacao
        self.payment_date = content_22_validated.valores.dataPagamento
        self.token = content_22_validated.token
        self.quote_currency_symbol = content_22_validated.valores.simboloMoedaCotacao
        self.quote_date = content_22_validated.valores.dataCotacao
        self.quantity_currency_traded = content_22_validated.valores.quantidadeMoedaNegociada
        self.spread_percentage = content_22_validated.valores.percentualSpread
        self.tax_value = content_22_validated.valores.valorTarifa
        self.total_effective_value = content_22_validated.valores.vet
        self.unique_id = unique_id

    def get_simulation_proposal_template(self):
        exchange_proposal_template = {
            "exchange_simulation_proposal": {
                "base_currency_symbol": self.base_currency_symbol,
                "commercial_fee": self.commercial_fee,
                "currency_quote_price": self.currency_quote_price,
                "client_id": self.client_id,
                "expiration_date": int(datetime.timestamp(self.expiration_date)),
                "client_fee": self.client_fee,
                "total_brl": self.gross_value,
                "iof_percentage": self.iof_percentage,
                "iof_value": self.iof_value,
                "net_value": self.net_value,
                "nature_operation_code": self.nature_operation_code,
                "payment_date": int(datetime.timestamp(self.payment_date)),
                "token": self.token,
                "quote_currency_symbol": self.quote_currency_symbol,
                "quote_date": int(datetime.timestamp(self.quote_date)),
                "total_usd": self.quantity_currency_traded,
                "spread_percentage": self.spread_percentage,
                "tax_value": self.tax_value,
                "total_effective_value": self.total_effective_value,
            }
        }
        return exchange_proposal_template

    def get_simulation_proposal_to_save_template(self):
        save_template = {
            "unique_id": self.unique_id,
            "base_currency_symbol": self.base_currency_symbol,
            "commercial_fee": self.commercial_fee,
            "currency_quote_price": self.currency_quote_price,
            "total_brl": self.gross_value,
            "client_id": self.client_id,
            "expiration_date": self.expiration_date,
            "client_fee": self.client_fee,
            "iof_percentage": self.iof_percentage,
            "iof_value": self.iof_value,
            "net_value": self.net_value,
            "nature_operation_code": self.nature_operation_code,
            "payment_date": self.payment_date,
            "token": self.token,
            "quote_currency_symbol": self.quote_currency_symbol,
            "quote_date": self.quote_date,
            "total_usd": self.quantity_currency_traded,
            "spread_percentage": self.spread_percentage,
            "tax_value": self.tax_value,
            "total_effective_value": self.total_effective_value,
        }
        return save_template
