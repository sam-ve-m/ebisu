# Ebisu
from src.domain.enums.response.internal_code import InternalCode
from src.domain.responses.http_response_model import ResponseModel
from src.domain.validators.forex_exchange.currency_options import CurrencyExchange
from src.domain.validators.forex_exchange.execution_exchange import ExchangeExecution
from src.services.jwt.service_jwt import JwtService
from src.services.forex_exchange.proposal_simulation.service import CustomerExchangeService
from src.services.forex_exchange.execute_proposal_simulation.service import ExecutionExchangeService

# Third party
from fastapi import Request, APIRouter, Depends, Response

# Standards
from http import HTTPStatus


class ForexExchange:

    __forex_exchange_router = APIRouter(prefix="/forex_exchange", tags=["Forex exchange"])

    @staticmethod
    def get_forex_exchange_router():
        return ForexExchange.__forex_exchange_router

    @staticmethod
    @__forex_exchange_router.get("/currency_exchange_simulation")
    async def get_exchange_simulation_proposal(
        request: Request, payload: CurrencyExchange = Depends()
    ) -> Response:
        jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
        result = await CustomerExchangeService.get_proposal_simulation(
            jwt_data=jwt_data,
            payload=payload
        )
        response = ResponseModel(
            success=True, result=result, internal_code=InternalCode.SUCCESS
        ).build_http_response(status_code=HTTPStatus.OK)
        return response

    @staticmethod
    @__forex_exchange_router.get("/execute_exchange_proposal")
    async def execute_exchange_simulation_proposal(
            request: Request, payload: ExchangeExecution) -> Response:
        jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
        success = await ExecutionExchangeService.execute_exchange_proposal(payload=payload, jwt_data=jwt_data)
        response = ResponseModel(
            success=success, internal_code=InternalCode.SUCCESS, message="Customer exchange proposal executed successfully"
        ).build_http_response(status_code=HTTPStatus.OK)
        return response
