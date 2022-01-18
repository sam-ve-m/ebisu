# STANDARD LIBS
import json
import logging
from typing import Optional

# OUTSIDE LIBRARIES
from fastapi import Response, status, Request

from api.utils.json_encoder.date_encoder import DateEncoder
from api.utils.jwt import validate_jwt


class BaseController:
    @staticmethod
    def run(callback: callable, payload: Optional[dict], request: Request) -> Response:
        jwt_validate = validate_jwt(request)
        if isinstance(jwt_validate, Response):
            return jwt_validate

        try:
            content, status_code = callback(payload).response()
        except Exception as error:
            logging.error(error)
            return Response(
                content=json.dumps(
                    {
                        "error": True,
                        "msg": str(error),
                        "status": status.HTTP_400_BAD_REQUEST,
                    }
                ),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        else:
            return Response(
                content=json.dumps(
                    {"data": content, "status": status_code}, cls=DateEncoder
                ),
                status_code=status_code,
            )
