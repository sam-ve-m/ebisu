from fastapi import APIRouter, FastAPI, Depends
import logging

from api.application_dependencies import (
    GLOBAL_APPLICATION_DEPENDENCIES,
    API_TITLE,
    API_DESCRIPTION,
)
from api.application_dependencies.singletons.mongo import MongoSingletonInstance
from api.application_dependencies.singletons.oracle import OracleSingletonInstance
from api.application_dependencies.singletons.s3 import S3SingletonInstance
from api.core.interfaces.interface import IService
from api.services.get_broker_note.get_broker_note import GetBrokerNote
from api.services.get_client_orders.get_client_orders import GetOrders
from api.services.get_statement.get_statement import GetStatement
from api.services.list_broker_note.list_broker_note import ListBrokerNote
from api.services.list_client_orders.list_client_orders import ListOrders
from api.services.list_client_orders.strategies import GetUsOrders, GetBrOrders
from api.services.get_client_orders.strategies import GetUsOrdersDetails, GetBrOrdersDetails
from api.services.request_statement.request_statement import RequestStatement

log = logging.getLogger()

router = APIRouter()

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    dependencies=GLOBAL_APPLICATION_DEPENDENCIES,
)


@app.get("/get_client_orders")
async def get_client_orders(service: IService = Depends(GetOrders)):
    GetUsOrdersDetails.oracle_singleton_instance = OracleSingletonInstance.get_oracle_us_singleton_instance()
    GetBrOrdersDetails.oracle_singleton_instance = OracleSingletonInstance.get_oracle_br_singleton_instance()
    return service.get_service_response()


@app.get("/list_client_orders")
async def get_client_orders(service: IService = Depends(ListOrders)):
    GetUsOrders.oracle_singleton_instance = OracleSingletonInstance.get_oracle_us_singleton_instance()
    GetBrOrders.oracle_singleton_instance = OracleSingletonInstance.get_oracle_br_singleton_instance()
    ListOrders.mongo_singleton = await MongoSingletonInstance.get_mongo_singleton_instance()
    return await service.get_service_response()


@app.get("/get_bank_statement")
async def get_bank_statement(service: IService = Depends(GetStatement)):
    GetStatement.oracle_singleton_instance = OracleSingletonInstance.get_statement_singleton_instance()
    return await service.get_service_response()


@app.get("/request_bank_statement")
async def request_bank_statement(service: IService = Depends(RequestStatement)):
    RequestStatement.oracle_singleton_instance = OracleSingletonInstance.get_statement_singleton_instance()
    RequestStatement.s3_singleton = S3SingletonInstance.get_s3_singleton_instance()
    return await service.get_service_response()


@app.get("/get_broker_note")
async def get_broker_note(service: IService = Depends(GetBrokerNote)):
    GetBrokerNote.s3_singleton = S3SingletonInstance.get_s3_singleton_instance()
    return service.get_service_response()


@app.get("/list_broker_note")
async def list_broker_note(service: IService = Depends(ListBrokerNote)):
    ListBrokerNote.s3_singleton = S3SingletonInstance.get_s3_singleton_instance()
    return service.get_service_response()
