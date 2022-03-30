# STANDARD LIBS
import json
import logging
from typing import Optional
from datetime import datetime

# OUTSIDE LIBRARIES
from fastapi import Response, status, Request
from api.services.jwt.service import validate_jwt
from nidavellir import Sindri
from api.core.interfaces.controllers.base_controller.interface import IController
from api.exceptions.exceptions import (
    UnauthorizedError,
    ForbiddenError,
    BadRequestError,
    InternalServerError,
)
from etria_logger import Gladsheim


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y/%m/%d %H:%M:%S")
        return json.JSONEncoder.default(self, obj)


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


class UserBaseController(IController):
    @staticmethod
    async def run(
        callback: callable, payload: Optional[dict], request: Request
    ) -> Response:
        try:
            response_metadata = await callback(payload)
            payload = await UserBaseController.create_response_payload(
                response_metadata=response_metadata
            )
            return Response(
                content=json.dumps(payload, default=Sindri.resolver),
                status_code=response_metadata.get("status_code"),
                headers={"Content-type": "application/json"},
            )
        except UnauthorizedError as e:
            return await UserBaseController.compile_error_response(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Error 401: Unauthorized",
            )
        except ForbiddenError as e:
            return await UserBaseController.compile_error_response(
                status_code=status.HTTP_403_FORBIDDEN,
                message="Error 403: Forbiden",
            )
        except BadRequestError as e:
            return await UserBaseController.compile_error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Register already exists",
            )
        except InternalServerError as e:
            return await UserBaseController.compile_error_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Error 500: Internal Server Error",
            )
        except Exception as e:
            Gladsheim.error(error=e)
            return await UserBaseController.compile_error_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Error 500: Internal Server Error",
            )

    @staticmethod
    async def compile_error_response(status_code: status, message: str):
        return Response(
            content=json.dumps({"detail": [{"msg": message}]}),
            status_code=status_code,
            headers={"Content-type": "application/json"},
        )

    @staticmethod
    async def create_response_payload(response_metadata: dict) -> dict:
        payload = dict()
        if "message_key" in response_metadata:
            payload.update(
                {
                    "message": "Account Created Successfully"
                }
            )
        if "payload" in response_metadata:
            payload.update(response_metadata.get("payload"))
        return payload
