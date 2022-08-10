from http import HTTPStatus
from typing import List, Tuple

from aiohttp import ClientResponse
from etria_logger import Gladsheim
from floki_client.src.transport.sinacor.transport import SinacorTransport

from src.domain.date_formatters.region.date_time.model import RegionStringDateTime
from src.domain.date_formatters.region.enum.date_format.enum import RegionDateFormat
from src.domain.date_formatters.region.enum.utc_offset.enum import ExchangeUtcOffset
from src.domain.earning.br.model import EarningBr
from src.infrastructures.env_config import config


class SinacorEarningsTransport:
    _floki_client = SinacorTransport(system_origin="ebisu")

    @staticmethod
    async def _process_response(response: ClientResponse) -> Tuple[bool, dict]:
        status = False
        body = {}
        if response.status in [HTTPStatus.OK, HTTPStatus.CREATED]:
            status = True
            body = await response.json()
        return status, body

    @classmethod
    async def paid_earnings(cls, client_accounts: Tuple[str]):
        try:
            url = config("PAID_EARNINGS_URL")
            futures = [
                cls._floki_client.get(url, query_params={
                    "filtro.contaDe": account,
                    "filtro.contaAte": account
                })
                for account in client_accounts
            ]
            responses = await asyncio.gather(*futures)
            process_response = [
                await cls._build_earnings_models(response=response)
                for response in responses
            ]
            client_accounts_response = dict(zip(client_accounts, process_response))
            return client_accounts_response
        except Exception as err:
            message = f"{cls.__class__}:paid_earnings"
            Gladsheim.error(error=err, message=message, client_accounts=client_accounts)
            raise

    @classmethod
    async def provisioned_earnings(cls, client_accounts: Tuple[str]):
        try:
            url = config("PROVISIONED_EARNINGS_URL")
            futures = [
                cls._floki_client.get(url, query_params={
                    "filtro.contaDe": account,
                    "filtro.contaAte": account
                })
                for account in client_accounts
            ]
            responses = await asyncio.gather(*futures)
            process_response = [
                await cls._build_earnings_models(response=response)
                for response in responses
            ]
            client_accounts_response = dict(zip(client_accounts, process_response))
            return client_accounts_response
        except Exception as err:
            message = f"{cls.__class__}:provisioned_earnings"
            Gladsheim.error(error=err, message=message, client_accounts=client_accounts)
            raise

    @staticmethod
    async def _build_earnings_models(response: ClientResponse) -> List[EarningBr]:
        earnings = list()
        if response.status in [HTTPStatus.OK, HTTPStatus.CREATED]:
            body = await response.json()
            if body and isinstance(body, list):
                for entity in body:
                    quantity = entity.get('quantidade', 0)
                    value = entity.get('valor', 0)
                    amount_per_share = 0
                    if quantity and value:
                        amount_per_share = value/quantity
                    earning = EarningBr(
                        symbol=entity.get("codigoNegociacao"),
                        description=entity.get('descricaoProvento', "NOT INFORMED"),
                        amount_per_share=amount_per_share,
                        share_quantity=quantity,
                        date=RegionStringDateTime(
                            date=entity.get("pagamento"),
                            utc_offset=ExchangeUtcOffset.BR_UTC_OFFSET,
                            region_date_format=RegionDateFormat.BR_DATE_ISO_FORMAT,
                        )
                    )
                    earnings.append(earning)
        return earnings


if __name__ == "__main__":
    import asyncio
    async def xxx():
        a = await SinacorEarningsTransport.provisioned_earnings(("8","10", "12", "71"))
        # b = await SinacorEarningsTransport.paid_earnings(("8","10", "12", "71"))
        print(a)
        # print(b)
    a = asyncio.run(xxx())
    print(a)