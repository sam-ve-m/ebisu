from api.domain.enums.region import Region
from fastapi import Request, APIRouter, Depends

from api.domain.validators.exchange_info_validators.client_orders_validator import GetClientOrderModel
from api.domain.validators.exchange_info_validators.earnings_validator import GetEarningsModel
from api.domain.validators.exchange_info_validators.get_balance_validator import GetBalanceModel
from api.domain.validators.exchange_info_validators.get_broker_note_validator import GetBrokerNoteModel
from api.domain.validators.exchange_info_validators.get_statement_validator import GetStatementModel
from api.domain.validators.exchange_info_validators.list_broker_note_validator import ListBrokerNoteModel
from api.domain.validators.exchange_info_validators.list_client_order_validator import ListClientOrderModel
from api.services.get_balance.get_balance import GetBalance
from api.services.get_broker_note.get_broker_note import GetBrokerNotePDF
from api.services.get_client_orders.get_client_orders import GetOrders
from api.services.get_earnings.get_client_earnings import EarningsService
from api.services.get_statement.get_statement import GetStatement
from api.services.jwt.service_jwt import JwtService
from api.services.list_broker_note.list_broker_note import ListBrokerNote
from api.services.list_client_orders.list_client_orders import ListOrders
from api.services.request_statement.request_statement import RequestStatement


class ExchangeRouter:

    __exchange_router = APIRouter()

    @staticmethod
    def get_exchange_router():
        return ExchangeRouter.__exchange_router

    @staticmethod
    @__exchange_router.get("/balance", tags=["Balance"])
    async def get_balance(
            request: Request, balance: GetBalanceModel = Depends()
    ):
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
            broker_note=broker_note, jwt_data=jwt_data)
        return broker_note_response

    @staticmethod
    @__exchange_router.get("/broker_note_pdf", tags=["Broker Note"])
    async def list_broker_note(
            request: Request, broker_note_pdf: GetBrokerNoteModel = Depends()
    ):
        jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
        broker_note_pdf_response = GetBrokerNotePDF.get_service_response(
            broker_note_pdf=broker_note_pdf, jwt_data=jwt_data
        )
        return broker_note_pdf_response

    @staticmethod
    @__exchange_router.get("/request_bank_statement_pdf", tags=["Bank Statement"])
    async def request_bank_RequestStatementstatement(
            region: Region, start_date: float, end_date: float, request: Request
    ):
        jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
        bank_statement_pdf_response = await RequestStatement.get_service_response(
            region=region, start_date=start_date, end_date=end_date, jwt_data=jwt_data
        )
        return bank_statement_pdf_response

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
    async def get_client_orders(
            request: Request, list_client_orders: ListClientOrderModel = Depends()
    ):
        jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
        list_client_orders_response = await ListOrders.get_service_response(
            list_client_orders=list_client_orders, jwt_data=jwt_data)
        return list_client_orders_response

    @staticmethod
    @__exchange_router.get("/earnings", tags=["Earnings"])
    async def get_br_earnings(
            earnings: GetEarningsModel = Depends()
    ):
        earnings_response = await EarningsService.get_service_response(
            earnings=earnings
        )
        return earnings_response
