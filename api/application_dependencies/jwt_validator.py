import logging
from typing import Union
from heimdall_client.bifrost import Heimdall
from fastapi import Request, status, HTTPException


CLIENT_JWT_NAME = "x-thebes-answer"
log = logging.getLogger()


async def verify_jwt_token_by_string(jwt: str) -> Union[Exception, dict]:
    heimdall = Heimdall(logger=log)
    jwt_content, heimdall_status = await heimdall.async_decode_payload(jwt=jwt)
    return jwt_content['decoded_jwt']


async def jwt_validator_and_decompile(request: Request) -> Union[Exception, dict]:
    jwt: str = request.headers.get(CLIENT_JWT_NAME)
    if jwt is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Jwt {CLIENT_JWT_NAME} not allowed"
        )

    return await verify_jwt_token_by_string(jwt)

