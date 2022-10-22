# Internal Libs
from http import HTTPStatus
from fastapi import FastAPI, Request

# ERRORS
from etria_logger import Gladsheim

from src.domain.enums.response.internal_code import InternalCode
from src.domain.exceptions.base_exceptions.model import (
    ServiceException,
    RepositoryException,
    DomainException,
    TransportException,
)

# ROUTERS
from src.routers.exchange_informations.router import ExchangeRouter
from src.routers.forex.router import ForexExchange
from src.routers.user_bank_accounts.router import UserBankAccountsRouter
from src.routers.funding_and_withdrawal.router import FundingAndWithdrawalRouter
from src.routers.user_portfolios.router import UserPortfoliosRouter

# MODELS
from src.domain.responses.http_response_model import ResponseModel


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
    def __register_forex_exchange():
        forex_exchange_router = ForexExchange.get_forex_exchange_router()
        BaseRouter.app.include_router(forex_exchange_router)
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
        BaseRouter.__register_forex_exchange()
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
        response = None

        try:
            response = await call_next(request)
        except ServiceException as err:
            Gladsheim.error(error=err, message=err.msg)
            response = ResponseModel(
                success=err.success, message=err.msg, internal_code=err.internal_code
            ).build_http_response(status_code=err.status_code)

        except DomainException as err:
            Gladsheim.error(error=err, message=err.msg)
            response = ResponseModel(
                success=err.success, message=err.msg, internal_code=err.internal_code
            ).build_http_response(status_code=err.status_code)

        except TransportException as err:
            Gladsheim.error(error=err, message=err.msg)
            response = ResponseModel(
                success=err.success, message=err.msg, internal_code=err.internal_code
            ).build_http_response(status_code=err.status_code)

        except RepositoryException as err:
            Gladsheim.error(error=err, message=err.msg)
            response = ResponseModel(
                success=err.success, message=err.msg, internal_code=err.internal_code
            ).build_http_response(status_code=err.status_code)

        except Exception as err:
            Gladsheim.error(erro=err)
            response = ResponseModel(
                success=False, message="An unexpected error occurred", internal_code=InternalCode.INTERNAL_SERVER_ERROR
            ).build_http_response(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
        finally:
            return response
