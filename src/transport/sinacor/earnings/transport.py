import datetime
from http import HTTPStatus
from typing import List, Tuple, NewType

from aiohttp import ClientResponse
from etria_logger import Gladsheim
from floki_client.src.transport.sinacor.transport import SinacorTransport

from src.domain.date_formatters.region.date_time.model import RegionStringDateTime
from src.domain.date_formatters.region.enum.date_format.enum import RegionDateFormat
from src.domain.date_formatters.region.enum.utc_offset.enum import ExchangeUtcOffset
from src.domain.earning.br.model import EarningBr
from src.infrastructures.env_config import config


PayableEarnings = NewType("PayableEarnings", List[EarningBr])
RecordDateEarnings = NewType("RecordDateEarnings", List[EarningBr])


class SinacorEarningsTransport:
    _floki_client = SinacorTransport(system_origin="ebisu")

    @classmethod
    async def paid_earnings(cls, account: str) -> List[EarningBr]:
        try:
            url = config("PAID_EARNINGS_URL")
            response = await cls._floki_client.get(
                url,
                query_params={"filtro.contaDe": account, "filtro.contaAte": account},
            )
            process_response = await cls._build_earnings_models(response=response)
            return process_response
        except Exception as err:
            message = f"{cls.__class__}:paid_earnings"
            Gladsheim.error(error=err, message=message, account=account)
            raise

    @classmethod
    async def payable_and_record_date_earnings(
        cls, account: str
    ) -> Tuple[PayableEarnings, RecordDateEarnings]:
        try:
            url = config("PROVISIONED_EARNINGS_URL")
            response = await cls._floki_client.get(
                url,
                query_params={"filtro.contaDe": account, "filtro.contaAte": account},
            )
            process_response = await cls._build_earnings_models(response=response)
            payable_earnings = list()
            record_date_earnings = list()
            for earning in process_response:
                if earning.date.date.year == 9999:
                    record_date_earnings.append(earning)
                else:
                    payable_earnings.append(earning)
            return PayableEarnings(payable_earnings), RecordDateEarnings(
                record_date_earnings
            )
        except Exception as err:
            message = f"{cls.__class__}:provisioned_earnings"
            Gladsheim.error(error=err, message=message, account=account)
            raise

    @staticmethod
    async def _build_earnings_models(response: ClientResponse) -> List[EarningBr]:
        earnings = list()
        if response.status in [HTTPStatus.OK, HTTPStatus.CREATED]:
            body = await response.json()
            if body and isinstance(body, list):
                for entity in body:
                    quantity = entity.get("quantidade", 0)
                    value = entity.get("valor", 0)
                    amount_per_share = 0
                    if quantity and value:
                        amount_per_share = value / quantity
                    earning = EarningBr(
                        symbol=entity.get("codigoNegociacao"),
                        description=entity.get("descricaoProvento", "NOT INFORMED"),
                        amount_per_share=amount_per_share,
                        share_quantity=quantity,
                        total=value,
                        date=RegionStringDateTime(
                            date=datetime.datetime.fromisoformat(
                                entity.get("pagamento")
                            ),
                            utc_offset=ExchangeUtcOffset.BR_UTC_OFFSET,
                            region_date_format=RegionDateFormat.BR_DATE_FORMAT,
                        ),
                    )
                    earnings.append(earning)
        return earnings
