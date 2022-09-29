# Third party
from etria_logger import Gladsheim
from jwt import JWT


class JwtForexService:

    @staticmethod
    async def decode(jwt_token):
        instance = JWT()
        algorithms = "HS256"
        try:
            jwt_data = instance.decode(
                message=jwt_token,
                algorithms=algorithms,
                do_verify=False,
            )
            return jwt_data
        except Exception as ex:
            Gladsheim.error(error=ex, message="error on trying to decode customer forex token")
            raise ex
