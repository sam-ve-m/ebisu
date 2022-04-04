# Internal Libs
from fastapi import Request, Response
from starlette import status
from api.domain.exception.model import IntegrityJwtError, AuthenticationJwtError
from etria_logger import Gladsheim
from api.core.interfaces.controllers.base_controller.interface import IController
from api.exceptions.exceptions import (
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
