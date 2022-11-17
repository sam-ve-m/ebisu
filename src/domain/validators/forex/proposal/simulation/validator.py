# Ebisu
from src.domain.date_formatters.region.enum.date_format.enum import RegionDateFormat
from src.domain.enums.forex.currency import CurrencyOptions
from src.domain.enums.forex.operations import NatureOperation
from src.domain.enums.forex.time_zones import TimeZones


# Third party
from pydantic import BaseModel, validator
from datetime import datetime
import pytz


class Tax(BaseModel):
    taxaComercial: float
    valorTotal: float


class ContentRoute21(BaseModel):
    token: str
    taxa: Tax


class Values(BaseModel):
    codigoCliente: int
    codigoNaturezaOperacao: NatureOperation
    simboloMoedaBase: CurrencyOptions
    simboloMoedaCotacao: CurrencyOptions
    quantidadeMoedaNegociada: float
    valorCotacaoCambio: float
    valorTarifa: float
    valorBruto: float
    percentualIOF: float
    valorIOF: float
    valorLiquido: float
    vet: float
    dataCotacao: datetime
    dataValidade: datetime
    dataPagamento: datetime
    percentualSpread: float
    taxaComercial: float

    @validator("dataCotacao", "dataValidade", "dataPagamento", pre=True)
    def parse_datetime_to_sao_paulo_timezone(cls, value):
        utc_datetime = datetime.strptime(
            value, RegionDateFormat.BR_DATE_ZULU_FORMAT.value
        )
        br_utc_datetime = pytz.utc.localize(utc_datetime).astimezone(
            tz=TimeZones.BR_SP.value
        )
        return br_utc_datetime


class ContentRoute22(BaseModel):
    token: str
    valores: Values
