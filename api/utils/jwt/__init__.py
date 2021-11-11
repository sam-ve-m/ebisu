import json
import logging
from typing import Optional
from fastapi import Response, Request, status
from heimdall_client.bifrost import Heimdall

log = logging.getLogger()
heimdall = Heimdall(logger=log)


def validate_jwt(request: Request) -> Optional[Response]:
    jwt_is_valid = heimdall.validate_jwt(jwt=request.headers.get('x-thebes-answer'))
    log.info(f"Jwt is valid {jwt_is_valid}")

    if not jwt_is_valid:
        return Response(
            content=json.dumps(
                {
                    "success": False,
                    "msg": "Authentication is not valid"
                }
            ),
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    return
