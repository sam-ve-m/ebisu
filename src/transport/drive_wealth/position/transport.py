import asyncio
import json
from typing import List

from etria_logger import Gladsheim
from mepho import DWApiTransport

from src.domain.exception import FailToGetDataFromTransportLayer
from src.domain.positions.model import Position
from src.infrastructures.env_config import config


class DwPositionTransport:
    __transport = DWApiTransport

    @classmethod
    async def get_positions(cls, accounts: List[str]) -> List[Position]:
        url = config("DW_POSITIONS_URL")
        positions = await cls.__execute_get(url=url, accounts=accounts, query_params={})
        return positions

    @classmethod
    async def __execute_get(
        cls, url, accounts: List[str], query_params: dict
    ) -> List[Position]:
        future_request = list()
        for account in accounts:
            url_formatted = url.format(account)
            future_request.append(
                cls.__transport.execute_get(
                    url=url_formatted, query_params=query_params
                )
            )
        responses = await asyncio.gather(*future_request)
        not_ok_responses = list(filter(lambda x: x.status != 200, responses))
        ok_responses = list(filter(lambda x: x.status == 200, responses))

        if not_ok_responses:
            Gladsheim.error(
                message=f"DwPositionTransport::__execute_get::Error error getting position from dw", responses_with_error=not_ok_responses
            )
            raise FailToGetDataFromTransportLayer

        all_positions = []
        for response in ok_responses:
            body_text = await response.text()
            body_json = json.loads(body_text)

            try:
                positions_dw = body_json['equityPositions']
                positions = cls.__consolidate_positions(positions_dw)
                all_positions += positions

            except Exception as error:
                dw_error = body_json.get("errorCode")
                dw_message = body_json.get("message")
                Gladsheim.error(
                    error=error,
                    message=f"DwPositionTransport::__execute_get::Error error getting position from dw",
                    dw_error=dw_error,
                    dw_message=dw_message
                )
                raise FailToGetDataFromTransportLayer

        return all_positions

    @staticmethod
    def __consolidate_positions(dw_positions: List[dict]) -> List[Position]:
        positions = list()
        for dw_position in dw_positions:
            positions.append(
                Position(
                    symbol=dw_position["symbol"],
                    quantity=dw_position["openQty"]
                )
            )
        return positions
