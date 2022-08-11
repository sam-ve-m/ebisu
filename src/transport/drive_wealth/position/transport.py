import asyncio
import json
from typing import List

from mepho import DWApiTransport
from etria_logger import Gladsheim

from src.domain.positions.model import Position
from src.infrastructures.env_config import config
from src.transport.drive_wealth.base.transport import DwBaseTransport


class DwPositionTransport(DwBaseTransport):

    __transport = DWApiTransport
    __positions_url = config("DW_POSITIONS_URL")

    @classmethod
    async def get_positions(cls, account: str) -> List[Position]:
        try:
            url_formatted = cls.__positions_url.format(account)
            response = await cls.__transport.execute_get(
                url=url_formatted, query_params={}
            )

            cls._handle_http_error_from_drive_wealth_request(
                request=url_formatted, response=response
            )

            body = await response.text()
            response = json.loads(body)

            cls._handle_dw_error_status_from_response(
                request=url_formatted, response=response
            )

            equity_positions = response["equityPositions"]
            positions = cls.__consolidate_positions(equity_positions)

            return positions

        except Exception as err:

            Gladsheim.error(
                message=f"DwBalanceTransport::get_balances::Error when get balance from drive wealth",
                error=err,
            )
            raise err

    @staticmethod
    def __consolidate_positions(equity_positions: List[dict]) -> List[Position]:
        positions = list()
        for equity_position in equity_positions:
            positions.append(
                Position(
                    symbol=equity_position["symbol"],
                    quantity=equity_position["openQty"],
                )
            )
        return positions
