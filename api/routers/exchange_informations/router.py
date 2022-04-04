# Internal Libs
from api.domain.enums.region import Region
from fastapi import Request, APIRouter

from api.services.get_balance.get_balance import GetBalance
from api.services.get_broker_note.get_broker_note import GetBrokerNotePDF
from api.services.jwt.service_jwt import JwtService
from api.services.list_broker_note.list_broker_note import ListBrokerNote


class ExchangeRouter:

    __exchange_router = APIRouter()

    @staticmethod
    def get_exchange_router():
        return ExchangeRouter.__exchange_router

    @staticmethod
    @__exchange_router.get("/balance", tags=["Balance"])
    async def get_balance(region: Region, request: Request):
        jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
        balance_response = await GetBalance.get_service_response(region=region, jwt_data=jwt_data)
        return balance_response

    @staticmethod
    @__exchange_router.get("/list_broker_note", tags=["Broker Note"])
    async def get_broker_note(region: Region, year, month, request: Request):
        jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
        broker_note_response = ListBrokerNote.get_service_response(
            region=region, year=year, month=month, jwt_data=jwt_data)
        return broker_note_response

    @staticmethod
    @__exchange_router.get("/broker_note_pdf", tags=["Broker Note"])
    async def list_broker_note(region: Region, year, month, day, request: Request):
        jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
        broker_note_pdf_response = GetBrokerNotePDF.get_service_response(
            region=region, year=year, month=month, day=day, jwt_data=jwt_data
        )
        return broker_note_pdf_response
