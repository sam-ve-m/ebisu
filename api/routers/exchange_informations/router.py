# Internal Libs
from api.domain.enums.region import Region
from fastapi import Request, APIRouter
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
            region: Region, request: Request
    ):
        jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
        balance_response = await GetBalance.get_service_response(region=region, jwt_data=jwt_data)
        return balance_response

    # still not working due to AWS has no correlated route yet
    @staticmethod
    @__exchange_router.get("/list_broker_note", tags=["Broker Note"])
    async def get_broker_note(
            region: Region, year: int, month: int, request: Request
    ):
        jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
        broker_note_response = ListBrokerNote.get_service_response(
            region=region, year=year, month=month, jwt_data=jwt_data)
        return broker_note_response

    @staticmethod
    @__exchange_router.get("/broker_note_pdf", tags=["Broker Note"])
    async def list_broker_note(
            region: Region, year: int, month: int, day: int, request: Request
    ):
        jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
        broker_note_pdf_response = GetBrokerNotePDF.get_service_response(
            region=region, year=year, month=month, day=day, jwt_data=jwt_data
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
            region: Region, limit: int, offset: int, start_date: float, end_date: float, request: Request
    ):
        jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
        bank_statement_response = await GetStatement.get_service_response(
            region=region, start_date=start_date, end_date=end_date, limit=limit, offset=offset, jwt_data=jwt_data
        )
        return bank_statement_response

    @staticmethod
    @__exchange_router.get("/client_orders", tags=["Client Orders"])
    async def get_client_orders(
            region: Region, cl_order_id: str, request: Request
    ):
        jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
        client_orders_response = GetOrders.get_service_response(
            region=region, cl_order_id=cl_order_id, jwt_data=jwt_data
        )
        return client_orders_response

    @staticmethod
    @__exchange_router.get("/list_client_orders", tags=["Client Orders"])
    async def get_client_orders(
            region: Region, limit: int, offset: int, order_status: str, request: Request
    ):
        jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
        list_client_orders_response = await ListOrders.get_service_response(
            region=region, limit=limit, offset=offset, order_status=order_status, jwt_data=jwt_data)
        return list_client_orders_response

    @staticmethod
    @__exchange_router.get("/earnings", tags=["Earnings"])
    async def get_br_earnings(
            symbol: str, timestamp: float, offset: int, limit: int
    ):
        earnings_response = await EarningsService.get_service_response(
            symbol=symbol, timestamp=timestamp, offset=offset, limit=limit
        )
        return earnings_response
