from fastapi import APIRouter, FastAPI, Request, Depends
import logging

from heimdall_client.bifrost import Heimdall

from api.application_dependencies import GLOBAL_APPLICATION_DEPENDENCIES, API_TITLE, API_DESCRIPTION
from api.core.interfaces.interface import IService
from api.domain.responses.get_client_orders import ResponseGetClientOrders
from api.services.get_client_orders.get_client_orders import GetOrders

log = logging.getLogger()

router = APIRouter()

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    dependencies=GLOBAL_APPLICATION_DEPENDENCIES
)


@app.get("/get_client_orders_faas", response_model=ResponseGetClientOrders)
async def get_client_orders(service: IService = Depends(GetOrders)):
    return service.get_service_response()
