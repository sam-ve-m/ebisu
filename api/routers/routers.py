import json
import logging
import codecs
"""
from fastapi import APIRouter, FastAPI, Depends, Request

from api.controller.base_controller import BaseController
from api.controller.exchange_information.get_balance_controller import GetBalanceController
from api.core.interfaces.interface import IService
from api.core.interfaces.bank_transfer.interface import IBankTransfer
from api.domain.enums.region import Region
from api.services.bank_transfer.service import BankTransferService
from api.services.get_broker_note.get_broker_note import GetBrokerNote
from api.services.get_client_orders.get_client_orders import GetOrders
from api.services.get_statement.get_statement import GetStatement
from api.services.list_broker_note.list_broker_note import ListBrokerNote
from api.services.list_client_orders.list_client_orders import ListOrders
from api.services.request_statement.request_statement import RequestStatement
from api.services.get_earnings.get_client_earnings import EarningsService
from api.controller.user_bank_accounts.controller import UserBankAccounts
from api.domain.validators.user_account_validators.bank_account import CreateUserBankAccount, UpdateUserBankAccounts, DeleteUsersBankAccount
from api.services.jwt.service_jwt import JwtService

from nidavellir import Sindri

@app.get("/client_orders", tags=["Client Orders"])
async def get_client_orders(service: IService = Depends(GetOrders)):
    client_orders_response = service.get_service_response()
    return client_orders_response

@app.get("/list_client_orders", tags=["Client Orders"])
async def get_client_orders(service: IService = Depends(ListOrders)):
    list_client_orders_response = await service.get_service_response()
    return list_client_orders_response

@app.get("/earnings", tags=["Earnings"])
async def get_br_earnings(service: IService = Depends(EarningsService)):
    earnings_response = await service.get_service_response()
    return earnings_response

@app.get("/bank_statement", tags=["Bank Statement"])
async def get_bank_statement(service: IService = Depends(GetStatement)):
    bank_statement_response = await service.get_service_response()
    return bank_statement_response

@app.get("/request_bank_statement_pdf", tags=["Bank Statement"])
async def request_bank_RequestStatementstatement(
    service: IService = Depends(RequestStatement),
):
    bank_statement_pdf_response = await service.get_service_response()
    return bank_statement_pdf_response

@app.get("/broker_note_pdf", tags=["Broker Note"])
async def get_broker_note(service: IService = Depends(GetBrokerNote)):
    broker_note_response = service.get_service_response()
    return broker_note_response

# ---------------- DONE   
@app.get("/list_broker_note", tags=["Broker Note"])
async def list_broker_note(service: IService = Depends(ListBrokerNote)):
    list_broker_note_response = service.get_service_response()
    return list_broker_note_response

# ---------------- DONE    
@app.get("/balance", tags=["Balance"])
async def get_balance(region: Region, request: Request):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
    payload = {
        "x-thebes-answer": jwt_data,
        "region": region
    }
    balace_data_response = await BaseController.run(
        GetBalanceController.get, payload, request)

    return balace_data_response

@app.get("/user/list_bank_accounts", tags=["User Bank Account"])
async def get_user_bank_accounts(request: Request):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
    payload = {
        "x-thebes-answer": jwt_data
    }
    get_user_bank_accounts_response = await BaseController.run(UserBankAccounts.get, payload, request)
    return get_user_bank_accounts_response

@app.post("/user/create_bank_account", tags=["User Bank Account"])
async def create_user_bank_accounts(create_bank_account: CreateUserBankAccount, request: Request):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
    payload = {
        "x-thebes-answer": jwt_data,
        "bank_account": create_bank_account.dict()
    }
    create_user_bank_accounts_response = await BaseController.run(UserBankAccounts.create, payload, request)
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
    update_bank_account_response = await BaseController.run(UserBankAccounts.update, payload, request)
    return update_bank_account_response

@app.delete("/user/delete_bank_account", tags=["User Bank Account"])
async def delete_bank_account(delete_account: DeleteUsersBankAccount, request: Request):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
    bank_account = delete_account.dict()
    payload = {
        "x-thebes-answer": jwt_data,
        "bank_account": bank_account
    }
    delete_bank_account_response = await BaseController.run(UserBankAccounts.delete, payload, request)
    return delete_bank_account_response

@app.get("/transfer", tags=["Bank Transfer"])
async def bank_transfer(
    request: Request, service: IBankTransfer = Depends(BankTransferService)
):
    bank_transfer_account_response = await service.get_bank_transfer_account(request)
    return bank_transfer_account_response
"""
