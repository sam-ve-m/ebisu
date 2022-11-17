# Ebisu
from src.domain.enums.response.internal_code import InternalCode
from src.domain.responses.http_response_model import ResponseModel
from src.domain.request.forex.currency_options import CurrencyExchange
from src.domain.request.forex.execution_proposal import ForexSimulationToken
from src.services.device_info.service import DeviceInfoService
from src.services.jwt.service import JwtService
from src.services.forex.proposal.simulation.service import ForexSimulation
from src.services.forex.proposal.execution.service import ForexExecution

# Third party
from fastapi import Request, APIRouter, Depends, Response

# Standards
from http import HTTPStatus


class ForexExchange:

    __forex_exchange_router = APIRouter(prefix="/forex", tags=["Foreign exchange"])

    @staticmethod
    def get_forex_exchange_router():
        return ForexExchange.__forex_exchange_router

    @staticmethod
    @__forex_exchange_router.get("/proposal_simulation")
    async def get_exchange_simulation_proposal(
        request: Request, payload: CurrencyExchange = Depends()
    ) -> Response:
        jwt_data = await JwtService.validate_and_decode_thebes_answer(request=request)
        device_info = await DeviceInfoService.get_device_info(request)
        result = await ForexSimulation.get_proposal_simulation(
            jwt_data=jwt_data, payload=payload,
            device_info=device_info
        )
        response = ResponseModel(
            success=True, result=result, internal_code=InternalCode.SUCCESS
        ).build_http_response(status_code=HTTPStatus.OK)
        return response

    @staticmethod
    @__forex_exchange_router.post("/execute_proposal")
    async def execute_exchange_simulation_proposal(
        request: Request, payload: ForexSimulationToken
    ) -> Response:
        jwt_data = await JwtService.validate_and_decode_thebes_answer(request=request)
        await JwtService.validate_mist(
            request=request, user_data=jwt_data["user"]
        )
        device_info = await DeviceInfoService.get_device_info(request)
        success = await ForexExecution.execute_proposal(
            payload=payload, jwt_data=jwt_data,
            device_info=device_info,
        )
        response = ResponseModel(
            success=success,
            internal_code=InternalCode.SUCCESS,
            message="Customer exchange proposal executed successfully",
        ).build_http_response(status_code=HTTPStatus.OK)
        return response
