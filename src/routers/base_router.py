# Internal Libs
from fastapi import FastAPI, Request, Response
from starlette import status
import json

# ERRORS
from src.domain.exception.model import IntegrityJwtError, AuthenticationJwtError
from etria_logger import Gladsheim
from src.exceptions.exceptions import (
    ForbiddenError,
    BadRequestError,
    InternalServerError,
    MoneyFlowResolverNoFoundError,
    InvalidAccountsOwnership,
    UnableToProcessMoneyFlow,
    NotMappedCurrency,
    InvalidElectronicaSignature,
)

# ROUTERS
from src.routers.exchange_informations.router import ExchangeRouter
from src.routers.user_bank_accounts.router import UserBankAccountsRouter
from src.routers.funding_and_withdrawal.router import FundingAndWithdrawalRouter
from src.routers.user_portfolios.router import UserPortfoliosRouter


class BaseRouter:

    app = FastAPI(
        title="Customer Exchange Information",
        description="Dados de clientes",
    )

    @staticmethod
    def __register_router_exchange():
        exchange_router = ExchangeRouter.get_exchange_router()
        BaseRouter.app.include_router(exchange_router)
        return BaseRouter.app

    @staticmethod
    def __register_router_account():
        user_bank_account_router = UserBankAccountsRouter.get_user_account_router()
        BaseRouter.app.include_router(user_bank_account_router)
        return BaseRouter.app

    @staticmethod
    def __register_funding_and_withdrawal():
        user_bank_account_router = FundingAndWithdrawalRouter.get_user_account_router()
        BaseRouter.app.include_router(user_bank_account_router)
        return BaseRouter.app

    @staticmethod
    def __register_user_portfolios():
        user_portfolios_router = UserPortfoliosRouter.get_user_portfolios_router()
        BaseRouter.app.include_router(user_portfolios_router)
        return BaseRouter.app

    @staticmethod
    def register_routers():
        BaseRouter.__register_router_exchange()
        BaseRouter.__register_router_account()
        BaseRouter.__register_funding_and_withdrawal()
        BaseRouter.__register_user_portfolios()

        return BaseRouter.app

    @staticmethod
    @app.middleware("http")
    async def middleware_response(request: Request, call_next: callable):
        middleware_service_response = await BaseRouter.__add_process_time_header(
            request=request, call_next=call_next
        )
        return middleware_service_response

    @staticmethod
    async def __add_process_time_header(request: Request, call_next):
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
                    {"request_status": False, "status": 5, "msg": e.args[0]}
                ),
            )

        except MoneyFlowResolverNoFoundError as e:
            return Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=json.dumps(
                    {"request_status": False, "status": 7, "msg": e.args[0]}
                ),
            )

        except InvalidAccountsOwnership as e:
            return Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=json.dumps(
                    {"request_status": False, "status": 8, "msg": e.args[0]}
                ),
            )

        except UnableToProcessMoneyFlow as e:
            return Response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=json.dumps(
                    {"request_status": False, "status": 8, "msg": e.args[0]}
                ),
            )

        except NotMappedCurrency as e:
            return Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=json.dumps(
                    {"request_status": False, "status": 9, "msg": e.args[0]}
                ),
            )

        except InvalidElectronicaSignature as e:
            return Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=json.dumps(
                    {"request_status": False, "status": 10, "msg": e.args[0]}
                ),
            )

        except Exception as err:
            Gladsheim.error(erro=err)
            return Response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=json.dumps(
                    {"request_status": False, "status": 6, "msg": err.args[0]}
                ),
            )

        return response
