# Ebisu
from src.domain.enums.forex.liquidation_date import LiquidationDayOptions
from src.domain.models.forex.proposal.execution_request_data.model import ExecutionModel
from src.domain.validators.forex.proposal.execution.validator import ContentRoute23

# Standards
from typing import Union

# Third party
from datetime import datetime


class OverseasBanker:
    def __init__(self, content_validated: ContentRoute23):
        self.ABA_code = (
            content_validated.operacaoCambio.dadosBanqueiroExterior.codigoABA
        )
        self.SWIFT_code = (
            content_validated.operacaoCambio.dadosBanqueiroExterior.codigoSWIFT
        )
        self.account_number = (
            content_validated.operacaoCambio.dadosBanqueiroExterior.numeroConta
        )
        self.beneficiary_name = (
            content_validated.operacaoCambio.dadosBanqueiroExterior.nomeBeneficiario
        )
        self.bank_name = (
            content_validated.operacaoCambio.dadosBanqueiroExterior.nomeBanco
        )


class LiquidationData:
    def __init__(self, content_validated: ContentRoute23):
        self.agency_number = (
            content_validated.operacaoCambio.dadosLiquidacao.numeroAgencia
        )
        self.account_number = (
            content_validated.operacaoCambio.dadosLiquidacao.numeroConta
        )
        self.account_digit = (
            content_validated.operacaoCambio.dadosLiquidacao.digitoConta
        )
        self.bank_number = content_validated.operacaoCambio.dadosLiquidacao.numeroBanco
        self.bank_name = content_validated.operacaoCambio.dadosLiquidacao.nomeBanco
        self.label = content_validated.operacaoCambio.dadosLiquidacao.rotulo


class ExecutionResponseModel:
    def __init__(
        self,
        unique_id,
        content_validated: ContentRoute23,
        execution_model: ExecutionModel,
    ):
        self.unique_id = unique_id
        self.client_id = content_validated.cliente.codigo
        self.token = execution_model.token
        self.liquidation_date = self.get_treated_datetime(
            execution_model=execution_model
        )
        self.exchange_operation_code = content_validated.operacaoCambio.codigo
        self.exchange_status_code = content_validated.operacaoCambio.status.codigo
        self.exchange_status_name = content_validated.operacaoCambio.status.nome
        self.nature_operation_code = (
            content_validated.operacaoCambio.naturezaOperacao.codigo
        )
        self.nature_operation_name = (
            content_validated.operacaoCambio.naturezaOperacao.nome
        )
        self.nature_operation_transaction_type = (
            content_validated.operacaoCambio.naturezaOperacao.tipoTransacao
        )
        self.nature_operation_mode = (
            content_validated.operacaoCambio.naturezaOperacao.modoOperacao
        )
        self.liquidation_data = self.build_liquidation_if_have_data(
            content_validated=content_validated
        )
        self.overseas_banker = self.build_overseas_bank_if_have_data(
            content_validated=content_validated
        )
        self.payment_currency_bacen_code = (
            content_validated.operacaoCambio.moedaPagamento.codigoBACEN
        )
        self.payment_currency_symbol = (
            content_validated.operacaoCambio.moedaPagamento.simbolo
        )
        self.traded_currency_bacen_code = (
            content_validated.operacaoCambio.moedaNegociada.codigoBACEN
        )
        self.traded_currency_symbol = (
            content_validated.operacaoCambio.moedaNegociada.simbolo
        )
        self.quantity_traded = content_validated.operacaoCambio.quantidadeNegociada
        self.payment_amount = content_validated.operacaoCambio.quantidadePagamento
        self.total_value = content_validated.operacaoCambio.valorTotal
        self.documents = content_validated.operacaoCambio.documentos
        self.IOF_percentage = content_validated.operacaoCambio.percentualIOF
        self.tariff = content_validated.operacaoCambio.tarifa
        self.control_code = content_validated.controle.codigo
        self.control_message = content_validated.controle.mensagem
        self.control_token = content_validated.controle.token
        self.control_datetime = content_validated.controle.dataHoraServidor

    @staticmethod
    def get_treated_datetime(execution_model: ExecutionModel) -> datetime:
        next_d2 = execution_model.stock_market.get_liquidation_date(
            day=LiquidationDayOptions.D2
        )
        next_d2_datetime = datetime.combine(next_d2, datetime.min.time())
        return next_d2_datetime

    @staticmethod
    def build_overseas_bank_if_have_data(
        content_validated: ContentRoute23,
    ) -> Union[None, OverseasBanker]:

        if not content_validated.operacaoCambio.dadosBanqueiroExterior:
            return None
        overseas_banker_model = OverseasBanker(content_validated=content_validated)
        return overseas_banker_model

    @staticmethod
    def build_liquidation_if_have_data(
        content_validated: ContentRoute23,
    ) -> Union[None, LiquidationData]:
        if not content_validated.operacaoCambio.dadosLiquidacao:
            return None
        liquidation_data = LiquidationData(content_validated=content_validated)
        return liquidation_data

    def get_execution_template_to_save(self) -> dict:
        execution_template_to_save = {
            "unique_id": self.unique_id,
            "client_id": self.client_id,
            "token": self.token,
            "exchange_operation_code": self.exchange_operation_code,
            "exchange_status_code": self.exchange_status_code,
            "exchange_status_name": self.exchange_status_name,
            "nature_operation_code": self.nature_operation_code,
            "nature_operation_name": self.nature_operation_name,
            "nature_operation_transaction_type": self.nature_operation_transaction_type,
            "nature_operation_mode": self.nature_operation_mode,
            "liquidation_date": self.liquidation_date,
            "liquidation_agency_number": self.liquidation_data.agency_number
            if self.liquidation_data
            else None,
            "liquidation_account_number": self.liquidation_data.account_number
            if self.liquidation_data
            else None,
            "liquidation_account_digit": self.liquidation_data.account_digit
            if self.liquidation_data
            else None,
            "liquidation_bank_number": self.liquidation_data.bank_number
            if self.liquidation_data
            else None,
            "liquidation_bank_name": self.liquidation_data.bank_name
            if self.liquidation_data
            else None,
            "liquidation_label": self.liquidation_data.label
            if self.liquidation_data
            else None,
            "overseas_banker_aba_code": self.overseas_banker.ABA_code
            if self.overseas_banker
            else None,
            "overseas_banker_swift_code": self.overseas_banker.SWIFT_code
            if self.overseas_banker
            else None,
            "overseas_banker_account_number": self.overseas_banker.account_number
            if self.overseas_banker
            else None,
            "overseas_banker_beneficiary_name": self.overseas_banker.beneficiary_name
            if self.overseas_banker
            else None,
            "overseas_banker_bank_name": self.overseas_banker.bank_name
            if self.overseas_banker
            else None,
            "payment_currency_bacen_code": self.payment_currency_bacen_code,
            "payment_currency_symbol": self.payment_currency_symbol,
            "traded_currency_bacen_code": self.traded_currency_bacen_code,
            "traded_currency_symbol": self.traded_currency_symbol,
            "quantity_traded": self.quantity_traded,
            "payment_amount": self.payment_amount,
            "total_value": self.total_value,
            "documents": self.documents,
            "IOF_percentage": self.IOF_percentage,
            "tariff": self.tariff,
            "control_code": self.control_code,
            "control_message": self.control_message,
            "control_token": self.control_token,
            "control_datetime": self.control_datetime,
        }
        return execution_template_to_save


