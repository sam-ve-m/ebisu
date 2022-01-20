from fastapi import APIRouter, FastAPI, Depends
import logging

from api.application_dependencies import (
    GLOBAL_APPLICATION_DEPENDENCIES,
    API_TITLE,
    API_DESCRIPTION,
)
from api.application_dependencies.singletons.mongo import MongoSingletonInstance
from api.application_dependencies.singletons.oracle import OracleSingletonInstance
from api.core.interfaces.interface import IService
from api.services.get_broker_note.get_broker_note import GetBrokerNote
from api.services.get_client_orders.get_client_orders import GetOrders
from api.services.get_statement.get_statement import GetStatement
from api.services.list_client_orders.list_client_orders import ListOrders
from api.services.list_client_orders.strategies import GetUsOrders, GetBrOrders
from api.services.get_client_orders.strategies import GetUsOrdersDetails, GetBrOrdersDetails

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


# @app.get("/request_bank_statement")
# async def request_bank_statement(service: IService = Depends(RequestStatement)):
#     GetStatement.oracle_singleton_instance = OracleSingletonInstance.get_statement_singleton_instance()
#     return await service.get_service_response()


@app.get("/get_broker_note")
async def get_broker_note(service: IService = Depends(GetBrokerNote)):
    GetStatement.oracle_singleton_instance = OracleSingletonInstance.get_statement_singleton_instance()
    return await service.get_service_response()

#
# @app.get("/request_broker_note")
# async def request_broker_note(service: IService = Depends(RequestBrokerNote)):
#     GetStatement.oracle_singleton_instance = OracleSingletonInstance.get_statement_singleton_instance()
#     return await service.get_service_response()