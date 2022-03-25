import logging
from typing import Union

from heimdall_client.bifrost import Heimdall
from fastapi import Request

from api.domain.exception.model import IntegrityJwtError, AuthenticationJwtError

CLIENT_JWT_NAME = "x-thebes-answer"
log = logging.getLogger()


async def verify_jwt_token_by_string(jwt: str) -> Union[Exception, dict]:
    jwt_content, heimdall_status = await Heimdall.decode_payload(jwt=jwt)
    jwt_heimdall = await Heimdall.validate_jwt_integrity(jwt, fields=["portfolios"])
    jwt_check_integrity = jwt_heimdall[0]['jwt_integrity']

    if jwt_check_integrity:
        return jwt_content['decoded_jwt']

    raise IntegrityJwtError(msg=f"The JWT was not allowed due to its integrity")


async def jwt_validator_and_decompile(request: Request) -> Union[Exception, dict]:
    jwt: str = request.headers.get(CLIENT_JWT_NAME)
    print(type(jwt))
    if jwt is None:
        raise AuthenticationJwtError(msg=f"The JWT was not allowed due to Authentication Error")

    return await verify_jwt_token_by_string(jwt)
