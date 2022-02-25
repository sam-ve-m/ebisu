import logging
from fastapi import APIRouter, FastAPI, Depends
from api.application_dependencies import (
    API_TITLE,
    API_DESCRIPTION,
)
from api.application_dependencies.singletons.mongo import MongoSingletonInstance
from api.application_dependencies.singletons.oracle import OracleSingletonInstance
from api.application_dependencies.singletons.s3 import S3SingletonInstance
from api.core.interfaces.interface import IService
from api.services.get_balance.get_balance import GetBalance
from api.services.get_broker_note.get_broker_note import GetBrokerNote
from api.services.get_client_orders.get_client_orders import GetOrders
from api.services.get_client_orders.strategies import GetUsOrdersDetails, GetBrOrdersDetails
from api.services.get_statement.get_statement import GetStatement
from api.services.list_broker_note.list_broker_note import ListBrokerNote
from api.services.list_client_orders.list_client_orders import ListOrders
from api.services.list_client_orders.strategies import GetUsOrders, GetBrOrders
from api.services.request_statement.request_statement import RequestStatement
from api.services.get_earnings.get_client_earnings import EarningsService
from api.services.get_earnings.strategies.br_earnings import GetBrEarnings


log = logging.getLogger()

router = APIRouter()

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
)


@app.get("/client_orders", tags=["Client Orders"])
async def get_client_orders(service: IService = Depends(GetOrders)):
    GetUsOrdersDetails.oracle_singleton_instance = OracleSingletonInstance.get_oracle_us_singleton_instance()
    GetBrOrdersDetails.oracle_singleton_instance = OracleSingletonInstance.get_oracle_br_singleton_instance()
    return service.get_service_response()


@app.get("/list_client_orders", tags=["Client Orders"])
async def get_client_orders(service: IService = Depends(ListOrders)):
    GetUsOrders.oracle_singleton_instance = OracleSingletonInstance.get_oracle_us_singleton_instance()
    GetBrOrders.oracle_singleton_instance = OracleSingletonInstance.get_oracle_br_singleton_instance()
    ListOrders.mongo_singleton = await MongoSingletonInstance.get_mongo_singleton_instance()
    return await service.get_service_response()


# ------------ doing this endpoint right now
@app.get("/earnings", tags=["Earnings"])
async def get_br_earnings(service: IService = Depends(EarningsService)):
    GetBrEarnings.oracle_earnings_singleton_instance = OracleSingletonInstance.get_earnings_singleton_instance()
    return await service.get_service_response()


@app.get("/balance", tags=["Balance"])
async def get_balance(service: IService = Depends(GetBalance)):
    GetBalance.oracle_singleton_instance = OracleSingletonInstance.get_statement_singleton_instance()
    return await service.get_service_response()


@app.get("/bank_statement", tags=["Bank Statement"])
async def get_bank_statement(service: IService = Depends(GetStatement)):
    GetStatement.oracle_singleton_instance = OracleSingletonInstance.get_statement_singleton_instance()
    return await service.get_service_response()


@app.get("/request_bank_statement_pdf", tags=["Bank Statement"])
async def request_bank_statement(service: IService = Depends(RequestStatement)):
    RequestStatement.oracle_singleton_instance = OracleSingletonInstance.get_statement_singleton_instance()
    RequestStatement.s3_singleton = S3SingletonInstance.get_s3_singleton_instance()
    return await service.get_service_response()


@app.get("/broker_note_pdf", tags=["Broker Note"])
async def get_broker_note(service: IService = Depends(GetBrokerNote)):
    GetBrokerNote.s3_singleton = S3SingletonInstance.get_s3_singleton_instance()
    return service.get_service_response()


@app.get("/list_broker_note", tags=["Broker Note"])
async def list_broker_note(service: IService = Depends(ListBrokerNote)):
    ListBrokerNote.s3_singleton = S3SingletonInstance.get_s3_singleton_instance()
    return service.get_service_response()
