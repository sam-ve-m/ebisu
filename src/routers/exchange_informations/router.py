# Standard Libs
from typing import List

from fastapi import Request, APIRouter, Depends

# MODELS
from src.domain.account_close_steps.response.model import AccountCloseStepsResponse
from src.domain.models.response.client_orders.response_model import ClientOrdersResponse
from src.domain.models.response.list_broker_note.response_model import (
    ListBrokerNoteBrResponse,
    ListBrokerNoteUsResponse,
    GetBrokerNoteUsResponse,
)
from src.domain.models.thebes_answer.model import ThebesAnswer
from src.domain.statement.br.response.model import (
    StatementResponse as BrStatementResponse,
)
from src.domain.statement.us.response.model import (
    StatementResponse as UsStatementResponse,
)
from src.domain.request.exchange_info.client_orders_validator import (
    GetClientOrderModel,
)
from src.domain.request.exchange_info.count_client_order_validator import (
    GetClientOrderQuantityModel,
)
from src.domain.request.exchange_info.get_closure_steps_validator import (
    AccountCloseStepsRequest,
)
from src.domain.request.exchange_info.get_earnings_client import EarningsClientModel
from src.domain.request.exchange_info.get_statement_validator import (
    GetBrStatement,
    GetUsStatement,
)
from src.domain.request.exchange_info.list_broker_note_validator import (
    ListBrokerNoteBrModel,
    ListBrokerNoteUsModel,
    GetBrokerNoteUsModel,
)
from src.domain.request.exchange_info.list_client_order_validator import (
    ListClientOrderModel,
)

# SERVICE IMPORTS
from src.services.account_close_steps.service import AccountCloseStepsService
from src.services.earnings_from_client.get_earnings_from_client import (
    EarningsFromClient,
)
from src.services.orders.orders import Orders
from src.services.statement.get_statement import GetStatement
from src.services.jwt.service import JwtService
from src.services.list_broker_note.list_broker_note import ListBrokerNote
from src.domain.models.response.list_client_orders.response_model import (
    ClientListOrdersResponse,
)
from src.domain.models.response.client_orders_quantity.response_model import (
    QuantityResponse,
)


class ExchangeRouter:

    __exchange_router = APIRouter()

    @staticmethod
    def get_exchange_router():
        return ExchangeRouter.__exchange_router

    @staticmethod
    @__exchange_router.get(
        "/list_broker_notes_br",
        tags=["Broker Note"],
        response_model=List[ListBrokerNoteBrResponse],
    )
    async def get_broker_notes_br(
        request: Request, broker_note: ListBrokerNoteBrModel = Depends()
    ):
        jwt_data = await JwtService.validate_and_decode_thebes_answer(request=request)
        thebes_answer = ThebesAnswer(jwt_data)
        broker_note_response = ListBrokerNote.get_list_broker_notes_br(
            thebes_answer=thebes_answer, broker_note=broker_note
        )
        return broker_note_response

    @staticmethod
    @__exchange_router.get(
        "/list_broker_notes_us",
        tags=["Broker Note"],
        response_model=List[ListBrokerNoteUsResponse],
    )
    async def list_broker_notes_us(
        request: Request, broker_note: ListBrokerNoteUsModel = Depends()
    ):
        jwt_data = await JwtService.validate_and_decode_thebes_answer(request=request)
        thebes_answer = ThebesAnswer(jwt_data)
        broker_note_response = await ListBrokerNote.list_broker_notes_us(
            thebes_answer=thebes_answer, broker_note=broker_note
        )
        return broker_note_response

    @staticmethod
    @__exchange_router.get(
        "/get_broker_note_us",
        tags=["Broker Note"],
        response_model=GetBrokerNoteUsResponse,
    )
    async def get_broker_note_us(
        request: Request, broker_note: GetBrokerNoteUsModel = Depends()
    ):
        jwt_data = await JwtService.validate_and_decode_thebes_answer(request=request)
        thebes_answer = ThebesAnswer(jwt_data)
        broker_note_response = await ListBrokerNote.get_broker_note_us(
            thebes_answer=thebes_answer, broker_note=broker_note
        )
        return broker_note_response

    @staticmethod
    @__exchange_router.get(
        "/br_bank_statement",
        response_model=BrStatementResponse,
        tags=["Bank Statement"],
    )
    async def get_bank_statement(
        request: Request, statement: GetBrStatement = Depends()
    ):
        jwt_data = await JwtService.validate_and_decode_thebes_answer(request=request)
        bank_statement_response = await GetStatement.get_br_bank_statement(
            statement=statement, jwt_data=jwt_data
        )
        return bank_statement_response

    @staticmethod
    @__exchange_router.get(
        "/us_bank_statement",
        response_model=UsStatementResponse,
        tags=["Bank Statement"],
    )
    async def get_bank_statement(
        request: Request, statement: GetUsStatement = Depends()
    ):
        jwt_data = await JwtService.validate_and_decode_thebes_answer(request=request)
        bank_statement_response = await GetStatement.get_us_bank_statement(
            statement=statement, jwt_data=jwt_data
        )
        return bank_statement_response

    @staticmethod
    @__exchange_router.get(
        "/client_orders",
        tags=["Client Orders"],
        response_model=List[ClientOrdersResponse],
    )
    async def get_client_orders(
        request: Request, client_order: GetClientOrderModel = Depends()
    ):
        jwt_data = await JwtService.validate_and_decode_thebes_answer(request=request)
        client_orders_response = Orders.get_client_orders(
            client_order=client_order, jwt_data=jwt_data
        )
        return client_orders_response

    @staticmethod
    @__exchange_router.get(
        "/list_client_orders",
        tags=["Client Orders"],
        response_model=List[ClientListOrdersResponse],
    )
    async def list_client_orders(
        request: Request, list_client_orders: ListClientOrderModel = Depends()
    ):
        jwt_data = await JwtService.validate_and_decode_thebes_answer(request=request)
        list_client_orders_response = await Orders.get_list_client_orders(
            jwt_data=jwt_data, list_client_orders=list_client_orders
        )
        return list_client_orders_response

    @staticmethod
    @__exchange_router.get(
        "/client_orders_quantity",
        tags=["Client Orders"],
        response_model=QuantityResponse,
    )
    async def get_client_orders(
        request: Request, client_order_quantity: GetClientOrderQuantityModel = Depends()
    ):
        jwt_data = await JwtService.validate_and_decode_thebes_answer(request=request)
        response = await Orders.get_client_orders_quantity(
            jwt_data=jwt_data, client_order_quantity=client_order_quantity
        )
        return response

    @staticmethod
    @__exchange_router.get("/earnings_client", tags=["Earnings"])
    async def get_earnings_from_client(
        request: Request, earnings_client: EarningsClientModel = Depends()
    ):
        jwt_data = await JwtService.validate_and_decode_thebes_answer(request=request)
        earnings_client_response = await EarningsFromClient.get_service_response(
            earnings_client=earnings_client, jwt_data=jwt_data
        )
        return earnings_client_response

    @staticmethod
    @__exchange_router.get(
        "/account_close_steps",
        response_model=AccountCloseStepsResponse,
        tags=["Account Close Steps"],
    )
    async def get_closure_steps(
        request: Request, closure_steps: AccountCloseStepsRequest = Depends()
    ):
        jwt_data = await JwtService.validate_and_decode_thebes_answer(request=request)
        closure_steps_response = await AccountCloseStepsService.get_service_response(
            closure_steps=closure_steps, jwt_data=jwt_data
        )
        return closure_steps_response
