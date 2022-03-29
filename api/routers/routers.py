import logging

from fastapi import APIRouter, FastAPI, Depends, Request, Response
from starlette import status

from api.infrastructures.application_dependencies import (
    API_TITLE,
    API_DESCRIPTION,
)
from api.core.interfaces.interface import IService
from api.services.get_balance.get_balance import GetBalance
from api.services.get_broker_note.get_broker_note import GetBrokerNote
from api.services.get_client_orders.get_client_orders import GetOrders
from api.services.get_statement.get_statement import GetStatement
from api.services.list_broker_note.list_broker_note import ListBrokerNote
from api.services.list_client_orders.list_client_orders import ListOrders
from api.services.request_statement.request_statement import RequestStatement
from api.services.get_earnings.get_client_earnings import EarningsService
from api.services.get_earnings.strategies.br_earnings import GetBrEarnings
from api.services.middleware.service import MiddlewareService
from etria_logger import Gladsheim


log = logging.getLogger()

router = APIRouter()

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
)


@app.middleware("http")
async def middleware_response(request: Request, call_next):
    response = await MiddlewareService.add_process_time_header(
        request=request,
        call_next=call_next)
    return response


@app.get("/client_orders", tags=["Client Orders"])
async def get_client_orders(service: IService = Depends(GetOrders)):
    teste = await service.get_service_response()
    return teste


@app.get("/list_client_orders", tags=["Client Orders"])
async def get_client_orders(service: IService = Depends(ListOrders)):
    return await service.get_service_response()


@app.get("/earnings", tags=["Earnings"])
async def get_br_earnings(service: IService = Depends(EarningsService)):
    return await service.get_service_response()


@app.get("/balance", tags=["Balance"])
async def get_balance(service: IService = Depends(GetBalance)):
    return await service.get_service_response()


@app.get("/bank_statement", tags=["Bank Statement"])
async def get_bank_statement(service: IService = Depends(GetStatement)):
    return await service.get_service_response()


@app.get("/request_bank_statement_pdf", tags=["Bank Statement"])
async def request_bank_RequestStatementstatement(service: IService = Depends(RequestStatement)):
    return await service.get_service_response()


@app.get("/broker_note_pdf", tags=["Broker Note"])
async def get_broker_note(service: IService = Depends(GetBrokerNote)):
    return service.get_service_response()


@app.get("/list_broker_note", tags=["Broker Note"])
async def list_broker_note(service: IService = Depends(ListBrokerNote)):
    return service.get_service_response()
