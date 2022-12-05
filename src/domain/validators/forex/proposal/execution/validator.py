# Ebisu
from src.domain.enums.forex.currency import CurrencyOptions

# Standards
from typing import Optional, Any, List

# Third party
from pydantic import BaseModel


class ExchangeStatus(BaseModel):
    codigo: int
    nome: str


class NatureOperation(BaseModel):
    codigo: int
    nome: Optional[str]
    tipoTransacao: str
    modoOperacao: str


class OverseasBanker(BaseModel):
    codigoABA: Optional[str]
    codigoSWIFT: str
    numeroConta: Optional[str]
    nomeBeneficiario: Optional[str]
    nomeBanco: str


class PaymentCurrency(BaseModel):
    codigoBACEN: int
    simbolo: CurrencyOptions


class TradedCurrency(BaseModel):
    codigoBACEN: int
    simbolo: CurrencyOptions


class Control(BaseModel):
    codigo: Optional[str]
    mensagem: Optional[str]
    token: Optional[Any]
    dataHoraServidor: Optional[str]


class LiquidationData(BaseModel):
    numeroAgencia: int
    numeroConta: int
    digitoConta: int
    numeroBanco: str
    nomeBanco: str
    rotulo: Optional[Any]


class ExchangeOperation(BaseModel):
    codigo: int
    status: ExchangeStatus
    naturezaOperacao: NatureOperation
    dadosLiquidacao: Optional[LiquidationData]
    dadosBanqueiroExterior: Optional[OverseasBanker]
    moedaPagamento: PaymentCurrency
    moedaNegociada: TradedCurrency
    quantidadeNegociada: Optional[float]
    quantidadePagamento: Optional[float]
    valorTotal: float
    documentos: Optional[List[Any]]
    percentualIOF: float
    tarifa: float


class ClientID(BaseModel):
    codigo: int


class ContentRoute23(BaseModel):
    cliente: ClientID
    operacaoCambio: ExchangeOperation
    controle: Control
