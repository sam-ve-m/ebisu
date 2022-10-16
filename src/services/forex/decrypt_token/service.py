# Ebisu
from src.domain.enums.forex.jwt_algorithms import Algorithms
from src.domain.exceptions.service.forex.exception import ErrorTryingToDecodeJwt

# Standards
from typing import Union

# Third party
from etria_logger import Gladsheim
from jwt import JWT


class DecryptService:
    @staticmethod
    async def decode(jwt_token) -> Union[dict, ErrorTryingToDecodeJwt]:
        instance = JWT()
        try:
            jwt_data = instance.decode(
                message=jwt_token,
                algorithms=Algorithms.HS256,
                do_verify=False,
            )
            return jwt_data
        except Exception as ex:
            Gladsheim.error(
                error=ex, message="error on trying to decode customer forex token"
            )
            raise ErrorTryingToDecodeJwt()
