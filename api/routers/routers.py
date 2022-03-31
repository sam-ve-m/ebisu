import logging

from fastapi import APIRouter, FastAPI, Depends, Request
from api.core.interfaces.interface import IService
from api.core.interfaces.bank_transfer.interface import IBankTransfer
from api.services.bank_transfer.service import BankTransferService
from api.services.get_balance.get_balance import GetBalance
from api.services.get_broker_note.get_broker_note import GetBrokerNote
from api.services.get_client_orders.get_client_orders import GetOrders
from api.services.get_statement.get_statement import GetStatement
from api.services.list_broker_note.list_broker_note import ListBrokerNote
from api.services.list_client_orders.list_client_orders import ListOrders
from api.services.request_statement.request_statement import RequestStatement
from api.services.get_earnings.get_client_earnings import EarningsService
from api.services.middleware.service import MiddlewareService
from api.services.jwt.service import jwt_validator_and_decompile

from nidavellir import Sindri

from api.controller.base_controller import BaseController, UserBaseController
from api.controller.user_bank_accounts.controller import UserBankAccounts
from api.domain.validators.bank_account import CreateUserBankAccount, UpdateUserBankAccounts, DeleteUsersBankAccount
from api.services.jwt.service_jwt import JwtService


log = logging.getLogger()

router = APIRouter()

app = FastAPI(
    title="Customer Exchange Information",
    description="Dados de clientes",
)


@app.middleware("http")
async def middleware_response(request: Request, call_next):
    response = await MiddlewareService.add_process_time_header(
        request=request, call_next=call_next
    )
    return response


@app.get("/client_orders", tags=["Client Orders"])
async def get_client_orders(service: IService = Depends(GetOrders)):
    response = service.get_service_response()
    return response


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
async def request_bank_RequestStatementstatement(
    service: IService = Depends(RequestStatement),
):
    return await service.get_service_response()


@app.get("/broker_note_pdf", tags=["Broker Note"])
async def get_broker_note(service: IService = Depends(GetBrokerNote)):
    return service.get_service_response()


@app.get("/list_broker_note", tags=["Broker Note"])
async def list_broker_note(service: IService = Depends(ListBrokerNote)):
    return service.get_service_response()


@app.get("/transfer", tags=["Bank Transfer"])
async def bank_transfer(
    request: Request, service: IBankTransfer = Depends(BankTransferService)
):
    bank_transfer_account_dict = await service.get_bank_transfer_account(request)
    return bank_transfer_account_dict


@app.get("/user/list_bank_accounts", tags=["User Bank Account"])
async def get_user_bank_accounts(request: Request):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
    payload = {
        "x-thebes-answer": jwt_data
    }
    get_user_bank_accounts_response = await UserBaseController.run(UserBankAccounts.get, payload, request)
    return get_user_bank_accounts_response


@app.post("/user/create_bank_account", tags=["User Bank Account"])
async def create_user_bank_accounts(create_bank_account: CreateUserBankAccount, request: Request):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
    payload = {
        "x-thebes-answer": jwt_data,
        "bank_account": create_bank_account.dict()
    }
    create_user_bank_accounts_response = await UserBaseController.run(UserBankAccounts.create, payload, request)
    return create_user_bank_accounts_response


@app.put("/user/update_bank_account", tags=["User Bank Account"])
async def update_bank_account(update_account: UpdateUserBankAccounts, request: Request):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
    bank_account = update_account.dict()
    Sindri.dict_to_primitive_types(obj=bank_account)
    payload = {
        "x-thebes-answer": jwt_data,
        "bank_account": bank_account
    }
    update_bank_account_response = await UserBaseController.run(UserBankAccounts.update, payload, request)
    return update_bank_account_response


@app.delete("/user/delete_bank_account", tags=["User Bank Account"])
async def delete_bank_account(delete_account: DeleteUsersBankAccount, request: Request):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
    bank_account = delete_account.dict()
    payload = {
        "x-thebes-answer": jwt_data,
        "bank_account": bank_account
    }
    delete_bank_account_response = await UserBaseController.run(UserBankAccounts.delete, payload, request)
    return delete_bank_account_response
