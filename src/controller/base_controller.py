# Internal Libs
from fastapi import Request
from starlette import status
from etria_logger import Gladsheim
from starlette.responses import Response
import json
from abc import ABC
from typing import Optional, Union

from src.core.interfaces.controllers.base_controller.interface import IController
from src.domain.exceptions import (
    UnauthorizedError,
    ForbiddenError,
    BadRequestError,
    InternalServerError,
)


class BaseController(IController, ABC):
    @staticmethod
    async def run(
        callback: callable, payload: Optional[dict], request: Request
    ) -> Union[dict, Response]:
        try:
            response_metadata = await callback(payload)

            payload = await BaseController.create_response_payload(
                response_metadata=response_metadata
            )
            return payload
            # return Response(
            #     content=json.dumps(payload, default=Sindri.resolver),
            #     status_code=response_metadata.get("status_code"),
            #     headers={"Content-type": "application/json"},
            # )

        except UnauthorizedError as e:
            error_response = await BaseController.compile_error_response(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Error 401: Unauthorized",
            )
            return error_response

        except ForbiddenError as e:
            error_response = await BaseController.compile_error_response(
                status_code=status.HTTP_403_FORBIDDEN,
                message="Error 403: Forbiden",
            )
            return error_response

        except BadRequestError as e:
            error_response = await BaseController.compile_error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Register already exists",
            )
            return error_response

        except InternalServerError as e:
            error_response = await BaseController.compile_error_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Error 500: Internal Server Error",
            )
            return error_response

        except Exception as e:
            Gladsheim.error(error=e)
            error_response = await BaseController.compile_error_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Error 500: Internal Server Error",
            )
            return error_response

    @staticmethod
    async def compile_error_response(status_code: status, message: str):
        error_response = Response(
            content=json.dumps({"detail": [{"msg": message}]}),
            status_code=status_code,
            headers={"Content-type": "application/json"},
        )
        return error_response

    @staticmethod
    async def create_response_payload(response_metadata: dict) -> dict:
        payload = dict()
        if "message_key" in response_metadata:
            payload.update({"message": "SUCCESS"})
        if "payload" in response_metadata:
            payload.update(response_metadata.get("payload"))

        return payload
