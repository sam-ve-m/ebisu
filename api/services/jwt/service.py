import json
from typing import Optional, Union
from fastapi import Response, Request, status
from heimdall_client.bifrost import Heimdall
from api.domain.exception.model import IntegrityJwtError, AuthenticationJwtError

heimdall = Heimdall()
CLIENT_JWT_NAME = "x-thebes-answer"


def validate_jwt(request: Request) -> Optional[Response]:
    jwt_is_valid = heimdall.validate_jwt(jwt=request.headers.get("x-thebs-answer"))
    if not jwt_is_valid:
        return Response(
            content=json.dumps(
                {"success": False, "msg": "Authentication is not valid"}
            ),
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    return


async def verify_jwt_token_by_string(jwt: str) -> Union[Exception, dict]:
    jwt_content, heimdall_status = await Heimdall.decode_payload(jwt=jwt)
    jwt_heimdall = await Heimdall.validate_jwt_integrity(jwt, fields=["portfolios"])
    jwt_check_integrity = jwt_heimdall[0]['jwt_integrity']

    if jwt_check_integrity:
        return jwt_content['decoded_jwt']

    raise IntegrityJwtError(msg=f"Jwt not allowed")


async def jwt_validator_and_decompile(request: Request) -> Union[Exception, dict]:
    jwt: str = request.headers.get(CLIENT_JWT_NAME)
    if jwt is None:
        raise AuthenticationJwtError(msg=f"Jwt not allowed")

    return await verify_jwt_token_by_string(jwt)