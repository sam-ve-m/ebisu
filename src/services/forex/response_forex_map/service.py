# Ebisu
from src.domain.exceptions.service.forex_exchange.exception import (
    UnexpectedErrorWhenTryingToGetExchangeSimulationProposal,
    ExpiredToken,
    InvalidToken,
    DroppedToken,
    CaronteCantFindToken,
)

# Standards
from typing import Union


# Third party
from caronte import CaronteStatus, CaronteStatusResponse


class ExchangeResponseMap:

    @classmethod
    async def get_response(
        cls, caronte_response: CaronteStatusResponse
    ) -> Union[dict, Exception]:
        success, caronte_status, content = caronte_response
        if caronte_status == CaronteStatus.SUCCESS:
            return content

        response_map = {
            CaronteStatus.BAD_REQUEST: ExpiredToken,
            CaronteStatus.UNAUTHORIZED: InvalidToken,
            CaronteStatus.FORBIDDEN: DroppedToken,
            CaronteStatus.TOKEN_NOT_FOUND: CaronteCantFindToken,
            CaronteStatus.UNEXPECTED_ERROR: UnexpectedErrorWhenTryingToGetExchangeSimulationProposal,
        }
        response_mapped = response_map.get(
            caronte_status, response_map.get(CaronteStatus.UNEXPECTED_ERROR)
        )
        await cls.__raise(exception=response_mapped)

    @staticmethod
    async def __raise(exception) -> Exception:
        raise exception()
