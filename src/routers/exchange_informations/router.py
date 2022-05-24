# Standard Libs
from fastapi import Request, APIRouter, Depends

# MODELS
from src.domain.validators.exchange_info.client_orders_validator import (
    GetClientOrderModel,
)
from src.domain.validators.exchange_info.get_balance_validator import GetBalanceModel
from src.domain.validators.exchange_info.get_earnings_client import EarningsClientModel
from src.domain.validators.exchange_info.get_statement_validator import (
    GetStatementModel,
)
from src.domain.validators.exchange_info.list_broker_note_validator import (
    ListBrokerNoteModel,
)
from src.domain.validators.exchange_info.list_client_order_validator import (
    ListClientOrderModel,
)

# SERVICE IMPORTS
from src.services.earnings_from_client.get_earnings_from_client import (
    EarningsFromClient,
)
from src.services.get_balance.service import GetBalance
from src.services.get_client_orders.get_client_orders import GetOrders
from src.services.get_statement.get_statement import GetStatement
from src.services.jwt.service_jwt import JwtService
from src.services.list_broker_note.list_broker_note import ListBrokerNote
from src.services.list_client_orders.list_client_orders import ListOrders


class ExchangeRouter:

    __exchange_router = APIRouter()

    @staticmethod
    def get_exchange_router():
        return ExchangeRouter.__exchange_router

    @staticmethod
    @__exchange_router.get("/balance", tags=["Balance"])
    async def get_balance(request: Request, balance: GetBalanceModel = Depends()):
        jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
        balance_response = await GetBalance.get_service_response(
            balance=balance, jwt_data=jwt_data
        )
        return balance_response

    # still not working due to AWS has no correlated route yet
    @staticmethod
    @__exchange_router.get("/list_broker_note", tags=["Broker Note"])
    async def get_broker_note(
        request: Request, broker_note: ListBrokerNoteModel = Depends()
    ):
        jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
        broker_note_response = ListBrokerNote.get_service_response(
            broker_note=broker_note, jwt_data=jwt_data
        )
        return broker_note_response

    @staticmethod
    @__exchange_router.get("/bank_statement", tags=["Bank Statement"])
    async def get_bank_statement(
        request: Request, statement: GetStatementModel = Depends()
    ):
        jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
        bank_statement_response = await GetStatement.get_service_response(
            statement=statement, jwt_data=jwt_data
        )
        return bank_statement_response

    @staticmethod
    @__exchange_router.get("/client_orders", tags=["Client Orders"])
    async def get_client_orders(
        request: Request, client_order: GetClientOrderModel = Depends()
    ):
        jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
        client_orders_response = GetOrders.get_service_response(
            client_order=client_order, jwt_data=jwt_data
        )
        return client_orders_response

    @staticmethod
    @__exchange_router.get("/list_client_orders", tags=["Client Orders"])
    async def list_client_orders(
        request: Request, list_client_orders: ListClientOrderModel = Depends()
    ):
        jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
        list_client_orders_response = await ListOrders.get_service_response(
            list_client_orders=list_client_orders, jwt_data=jwt_data
        )
        return list_client_orders_response

    @staticmethod
    @__exchange_router.get("/earnings_client", tags=["Earnings"])
    async def get_earnings_from_client(
        request: Request, earnings_client: EarningsClientModel = Depends()
    ):
        jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
        earnings_client_response = EarningsFromClient.get_service_response(
            earnings_client=earnings_client, jwt_data=jwt_data
        )
        return earnings_client_response
