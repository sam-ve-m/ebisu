# Ebisu

# Standards
from typing import Union


# Third party
from caronte import CaronteStatus, CaronteStatusResponse

from src.domain.exceptions.service.forex.model import (
    ExpiredToken,
    InvalidToken,
    DroppedToken,
    CaronteCantFindToken,
    UnexpectedErrorInExchangeAPI,
)


class ForexResponseMap:
    @classmethod
    async def get_response(
        cls, caronte_response: CaronteStatusResponse
    ) -> Union[dict, Exception]:
        success, caronte_status, content = caronte_response
        if caronte_status == CaronteStatus.SUCCESS:
            return content
        """
            Alguns erros estão retornando de forma incorreta pela OuroInvest, trazendo o  status code 400 Bad Request
            para diversas situações das quais não deveriam, exemplos:
                - Ao dropar o token batendo pelo postman e continuar a execução do código, retorna bad_request, deveria ser um forbidden
                - Ao alterar o JWT/TOKEN da OuroInvest, deixando ele inválido, retorna bad_reqquest, deveria ser thebes_answer
                - Um cenário muito específico retorna erro de natureza de operação com status bad_request (mesmo ela não sendo alterada),
                 deveria ser forbidden para token dropado       
        """
        response_map = {
            CaronteStatus.BAD_REQUEST: ExpiredToken,
            CaronteStatus.UNAUTHORIZED: InvalidToken,
            CaronteStatus.FORBIDDEN: DroppedToken,
            CaronteStatus.TOKEN_NOT_FOUND: CaronteCantFindToken,
            CaronteStatus.UNEXPECTED_ERROR: UnexpectedErrorInExchangeAPI,
        }
        response_mapped = response_map.get(
            caronte_status, response_map.get(CaronteStatus.UNEXPECTED_ERROR)
        )
        await cls.__raise(exception=response_mapped)

    @staticmethod
    async def __raise(exception) -> Exception:
        raise exception()
