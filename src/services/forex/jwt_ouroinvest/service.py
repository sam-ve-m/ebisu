# Third party
from etria_logger import Gladsheim
import jwt


class JwtService:

    @staticmethod
    async def decode_jwt_token(jwt_data: str) -> dict:
        options = {"verify_signature": False}
        algorithms = ["HS256"]
        try:
            jwt_decoded = jwt.decode(
                jwt=jwt_data,
                algorithms=algorithms,
                options=options
            )
            return jwt_decoded
        except Exception as ex:
            Gladsheim.error(error=ex, message="error on trying to decode customer forex token")
            raise ex
