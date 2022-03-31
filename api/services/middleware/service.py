# Internal Libs
from fastapi import Request, Response
from starlette import status
from api.domain.exception.model import IntegrityJwtError, AuthenticationJwtError
from etria_logger import Gladsheim
from nidavellir import Sindri
from api.core.interfaces.controllers.base_controller.interface import IController
from api.exceptions.exceptions import (
    UnauthorizedError,
    ForbiddenError,
    BadRequestError,
    InternalServerError,
)

# STANDARD LIBS
import json
from abc import ABC
from typing import Optional


class MiddlewareService(IController, ABC):
    @staticmethod
    async def add_process_time_header(request: Request, call_next):
        try:
            response = await call_next(request)

        except IntegrityJwtError as err:
            Gladsheim.error(erro=err)

            return Response(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=json.dumps(
                    {"request_status": False, "status": 1, "msg": err.args[0]}
                ),
            )

        except AuthenticationJwtError as err:
            Gladsheim.error(erro=err)
            return Response(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=json.dumps(
                    {"request_status": False, "status": 2, "msg": err.args[0]}
                ),
            )

        except ForbiddenError as e:
            return Response(
                status_code=status.HTTP_403_FORBIDDEN,
                content=json.dumps(
                    {"request_status": False, "status": 3, "msg": e.args[0]}
                ),
            )

        except BadRequestError as e:
            return Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=json.dumps(
                    {"request_status": False, "status": 4, "msg": e.args[0]}
                ),
            )
        except InternalServerError as e:
            return Response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=json.dumps(
                    {"request_status": False, "status": 4, "msg": e.args[0]}
                ),
            )

        except Exception as err:
            Gladsheim.error(erro=err)
            return Response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=json.dumps(
                    {"request_status": False, "status": 3, "msg": err.args[0]}
                ),
            )

        return response

    @staticmethod
    async def run(
            callback: callable, payload: Optional[dict], request: Request
    ) -> Response:
        try:
            response_metadata = await callback(payload)

            payload = await MiddlewareService.create_response_payload(
                response_metadata=response_metadata
            )
            return Response(
                content=json.dumps(payload, default=Sindri.resolver),
                status_code=response_metadata.get("status_code"),
                headers={"Content-type": "application/json"},
            )

        except UnauthorizedError as e:
            return await MiddlewareService.compile_error_response(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Error 401: Unauthorized",
            )

        except ForbiddenError as e:
            return await MiddlewareService.compile_error_response(
                status_code=status.HTTP_403_FORBIDDEN,
                message="Error 403: Forbiden",
            )

        except BadRequestError as e:
            return await MiddlewareService.compile_error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Register already exists",
            )

        except InternalServerError as e:
            return await MiddlewareService.compile_error_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Error 500: Internal Server Error",
            )

        except Exception as e:
            Gladsheim.error(error=e)
            return await MiddlewareService.compile_error_response(
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
                    "message": "SUCCESS"
                }
            )
        if "payload" in response_metadata:
            payload.update(response_metadata.get("payload"))

        return payload


# class DateEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, datetime):
#             return obj.strftime("%Y/%m/%d %H:%M:%S")
#         return json.JSONEncoder.default(self, obj)
