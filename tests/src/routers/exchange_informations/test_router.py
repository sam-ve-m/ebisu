# Standard Libs
import pytest
from unittest.mock import patch, MagicMock
from pydantic import ValidationError

# INTERNAL LIBS
from src.domain.enums.region import Region
from src.domain.validators.exchange_info.client_orders_validator import (
    GetClientOrderModel,
)
from src.domain.validators.exchange_info.earnings_validator import GetEarningsModel
from src.domain.validators.exchange_info.get_balance_validator import GetBalanceModel
from src.domain.validators.exchange_info.get_earnings_client import EarningsClientModel
from src.domain.validators.exchange_info.get_statement_validator import (
    GetStatementModel,
)
from src.domain.validators.exchange_info.list_broker_note_validator import (
    BrokerNoteRegion,
    BrokerNoteMarket,
    ListBrokerNoteModel,
)
from src.domain.validators.exchange_info.list_client_order_validator import (
    ListClientOrderModel,
)
from src.routers.exchange_informations.router import ExchangeRouter
from src.services.earnings_from_client.get_earnings_from_client import EarningsFromClient
from src.services.get_balance.service import GetBalance
from src.exceptions.exceptions import UnauthorizedError
from src.services.get_client_orders.get_client_orders import GetOrders
from src.services.get_earnings.get_client_earnings import EarningsService
from src.services.get_statement.get_statement import GetStatement
from src.services.jwt.service_jwt import JwtService
from src.services.list_broker_note.list_broker_note import ListBrokerNote
from src.services.list_client_orders.list_client_orders import ListOrders

# stubs
from tests.src.stubs.project_stubs.stub_earnings import earnings_dummy_response
from tests.src.stubs.project_stubs.stub_get_client_orders import (
    client_order_response_dummy,
)
from tests.src.stubs.project_stubs.stub_list_client_orders import (
    stub_expected_response,
    client_response,
)
from tests.src.stubs.project_stubs.stub_data import payload_data_dummy
from tests.src.stubs.router_exchange_infos.stubs import (
    balance_stub,
    scope_stub_2,
    x_thebes_tuple,
    scope_stub,
    list_broker_note_stub,
    statement_stub,
)


@pytest.mark.asyncio
@patch.object(
    JwtService, "get_thebes_answer_from_request", return_value=payload_data_dummy
)
@patch.object(GetBalance, "get_service_response", return_value=balance_stub)
async def test_when_sending_the_right_params_to_get_balance_then_return_the_expected(
    mock_get_thebes_answer_from_request, mock_get_service_response
):
    response = await ExchangeRouter.get_balance(
        request=MagicMock(scope=scope_stub_2, headers=MagicMock(raw=x_thebes_tuple)),
        balance=GetBalanceModel(**{"region": "BR"}),
    )

    assert response == balance_stub
    assert "payload" in response
    assert response.get("payload").get("balance") == 49030153.7
    assert isinstance(response, dict)


@pytest.mark.asyncio
@patch(
    "src.routers.exchange_informations.router.GetBalance.get_service_response",
    return_value={},
)
@patch.object(
    JwtService, "get_thebes_answer_from_request", return_value=payload_data_dummy
)
async def test_when_sending_the_right_params_to_get_balance_then_return_an_empty_list_as_expected(
    mock_get_thebes_answer_from_request, mock_get_service_response
):

    response = await ExchangeRouter.get_balance(
        request=MagicMock(scope=scope_stub_2, headers=MagicMock(raw=x_thebes_tuple)),
        balance=GetBalanceModel(**{"region": "BR"}),
    )

    assert response == {}
    assert isinstance(response, dict)


@pytest.mark.asyncio
async def test_when_sending_wrong_params_of_region_to_get_balance_then_raise_validation_error():

    with pytest.raises(ValidationError):
        await ExchangeRouter.get_balance(
            request=MagicMock(
                scope=scope_stub_2, headers=MagicMock(raw=x_thebes_tuple)
            ),
            balance=GetBalanceModel(**{"region": None}),
        )


@pytest.mark.asyncio
async def test_when_sending_the_wrong_payload_jwt_invalid_to_get_balance_then_raise_unauthorized_error():

    with pytest.raises(UnauthorizedError):
        await ExchangeRouter.get_balance(
            request=MagicMock(scope=scope_stub),
            balance=GetBalanceModel(**{"region": "BR"}),
        )


# list broker note router
@pytest.mark.asyncio
@patch.object(
    JwtService, "get_thebes_answer_from_request", return_value=payload_data_dummy
)
@patch.object(
    ListBrokerNote, "get_service_response", return_value=list_broker_note_stub
)
async def test_when_sending_the_right_params_to_get_list_broker_note_then_return_the_expected(
    mock_get_thebes_answer_from_request, mock_get_service_response
):
    link_response_stub = "https://brokerage-note-and-bank-statement.s3.amazonaws.com/14/BR/broker_note/2022/4/5.pdf?AWS"

    response = await ExchangeRouter.get_broker_note(
        request=MagicMock(scope=scope_stub_2, headers=MagicMock(raw=x_thebes_tuple)),
        broker_note=ListBrokerNoteModel(
            **{
                "region": BrokerNoteRegion.BR.value,
                "market": BrokerNoteMarket.BMF.value,
                "year": 2022,
                "month": 4,
            }
        ),
    )
    assert response == list_broker_note_stub
    assert response[0].get("broker_note_link") == link_response_stub


@pytest.mark.asyncio
@patch.object(
    JwtService, "get_thebes_answer_from_request", return_value=payload_data_dummy
)
@patch.object(ListBrokerNote, "get_service_response", return_value=[])
async def test_when_sending_the_right_params_to_get_list_broker_note_then_return_the_an_empty_list(
    mock_mock_get_thebes_answer_from_request, mock_get_service_response
):
    list_broker_response = await ExchangeRouter.get_broker_note(
        request=MagicMock(scope=scope_stub_2, headers=MagicMock(raw=x_thebes_tuple)),
        broker_note=ListBrokerNoteModel(
            **{
                "region": BrokerNoteRegion.BR.value,
                "market": BrokerNoteMarket.BOVESPA.value,
                "year": 2018,
                "month": 1,
            }
        ),
    )
    assert list_broker_response == []
    assert isinstance(list_broker_response, list)


@pytest.mark.asyncio
async def test_when_sending_wrong_params_of_list_broker_note_model_to_get_broker_note_then_raise_validation_error():

    with pytest.raises(ValidationError):
        await ExchangeRouter.get_broker_note(
            request=MagicMock(
                scope=scope_stub_2, headers=MagicMock(raw=x_thebes_tuple)
            ),
            broker_note=ListBrokerNoteModel(
                **{"region": None, "market": None, "year": 2018, "month": 1}
            ),
        )


@pytest.mark.asyncio
async def test_when_sending_the_wrong_payload_jwt_invalid_to_broker_note_router_then_raise_unauthorized_error():

    with pytest.raises(UnauthorizedError):
        await ExchangeRouter.get_broker_note(
            request=MagicMock(scope=scope_stub),
            broker_note=ListBrokerNoteModel(
                **{
                    "region": BrokerNoteRegion.BR.value,
                    "market": BrokerNoteMarket.BOVESPA.value,
                    "year": 2018,
                    "month": 1,
                }
            ),
        )


# bank statement router
@pytest.mark.asyncio
@patch.object(
    JwtService, "get_thebes_answer_from_request", return_value=payload_data_dummy
)
@patch.object(GetStatement, "get_service_response", return_value=statement_stub)
async def test_when_sending_the_right_params_to_bank_statement_then_return_the_expected(
    mock_get_thebes_answer_from_request, mock_get_service_response
):
    response_statement = await ExchangeRouter.get_bank_statement(
        request=MagicMock(scope=scope_stub_2, headers=MagicMock(raw=x_thebes_tuple)),
        statement=GetStatementModel(
            **{
                "region": BrokerNoteRegion.BR.value,
                "limit": 1,
                "offset": 0,
                "start_date": 1646757399000,
                "end_date": 1648485399000,
            }
        ),
    )

    assert response_statement == statement_stub


@pytest.mark.asyncio
async def test_when_sending_wrong_params_of_get_statement_model_then_raise_validation_error():

    with pytest.raises(ValidationError):
        await ExchangeRouter.get_bank_statement(
            request=MagicMock(
                scope=scope_stub_2, headers=MagicMock(raw=x_thebes_tuple)
            ),
            statement=GetStatementModel(
                **{
                    "region": None,
                    "limit": 1,
                    "offset": 0,
                    "start_date": None,
                    "end_date": None,
                }
            ),
        )


@pytest.mark.asyncio
async def test_when_sending_the_wrong_payload_jwt_invalid_to_get_statement_router_then_raise_unauthorized_error():

    with pytest.raises(UnauthorizedError):
        await ExchangeRouter.get_bank_statement(
            request=MagicMock(scope=scope_stub_2),
            statement=GetStatementModel(
                **{
                    "region": BrokerNoteRegion.BR.value,
                    "limit": 1,
                    "offset": 0,
                    "start_date": 1646757399000,
                    "end_date": 1648485399000,
                }
            ),
        )


# get client orders router
@pytest.mark.asyncio
@patch.object(
    JwtService, "get_thebes_answer_from_request", return_value=payload_data_dummy
)
@patch.object(
    GetOrders, "get_service_response", return_value=client_order_response_dummy
)
async def test_when_sending_the_right_params_to_client_order_router_then_return_the_expected(
    mock_get_thebes_answer_from_request, mock_get_service_response
):

    response = await ExchangeRouter.get_client_orders(
        request=MagicMock(scope=scope_stub_2, headers=MagicMock(raw=x_thebes_tuple)),
        client_order=GetClientOrderModel(
            **{
                "region": Region.BR.value,
                "cl_order_id": "008cf873-ee2a-4b08-b277-74b8b17f6e64",
            }
        ),
    )

    assert response == client_order_response_dummy
    assert response[0].get("symbol") == "VALE3"


@pytest.mark.asyncio
async def test_when_sending_wrong_params_to_get_client_orders_router_then_raise_validation_error():

    with pytest.raises(ValidationError):
        await ExchangeRouter.get_client_orders(
            request=MagicMock(
                scope=scope_stub_2, headers=MagicMock(raw=x_thebes_tuple)
            ),
            client_order=GetClientOrderModel(**{"region": None, "cl_order_id": None}),
        )


@pytest.mark.asyncio
async def test_when_sending_the_wrong_payload_jwt_invalid_to_get_client_orders_router_then_raise_unauthorized_error():

    with pytest.raises(UnauthorizedError):
        await ExchangeRouter.get_client_orders(
            request=MagicMock(scope=scope_stub),
            client_order=GetClientOrderModel(
                **{
                    "region": Region.BR.value,
                    "cl_order_id": "008cf873-ee2a-4b08-b277-74b8b17f6e64",
                }
            ),
        )


# list client orders router
@pytest.mark.asyncio
@patch.object(
    JwtService, "get_thebes_answer_from_request", return_value=payload_data_dummy
)
@patch.object(ListOrders, "get_service_response", return_value=client_response)
async def test_when_sending_the_right_params_to_list_client_order_router_then_return_the_expected(
    mock_get_thebes_answer_from_request, mock_get_service_response
):
    response = await ExchangeRouter.list_client_orders(
        request=MagicMock(scope=scope_stub_2, headers=MagicMock(raw=x_thebes_tuple)),
        list_client_orders=ListClientOrderModel(
            **{
                "region": Region.BR.value,
                "limit": 1,
                "offset": 0,
                "order_status": "FILLED",
            }
        ),
    )

    assert response == stub_expected_response
    assert response[0].get("name") == "CannaPharmaRx Inc"


@pytest.mark.asyncio
async def test_when_sending_wrong_params_to_list_client_orders_router_then_raise_validation_error():

    with pytest.raises(ValidationError):
        await ExchangeRouter.list_client_orders(
            request=MagicMock(
                scope=scope_stub_2, headers=MagicMock(raw=x_thebes_tuple)
            ),
            list_client_orders=ListClientOrderModel(
                **{"region": None, "limit": 1, "offset": 0, "order_status": None}
            ),
        )


@pytest.mark.asyncio
async def test_when_sending_the_wrong_payload_jwt_invalid_to_list_client_orders_router_then_raise_unauthorized_error():

    with pytest.raises(UnauthorizedError):
        await ExchangeRouter.list_client_orders(
            request=MagicMock(scope=scope_stub_2),
            list_client_orders=ListClientOrderModel(
                **{
                    "region": Region.BR.value,
                    "limit": 1,
                    "offset": 0,
                    "order_status": "FILLED",
                }
            ),
        )


# earnings router
@pytest.mark.asyncio
@patch.object(
    EarningsService, "get_service_response", return_value=earnings_dummy_response
)
async def test_when_sending_the_right_params_to_earnings_router_then_return_the_expected(
    mock_get_service_response,
):

    response = await ExchangeRouter.get_br_earnings(
        earnings=GetEarningsModel(
            **{"symbol": "PETR4", "limit": 1, "offset": 0, "timestamp": 1646757399000}
        )
    )

    assert response == earnings_dummy_response
    assert response[0].get("price") == 299


@pytest.mark.asyncio
@patch.object(EarningsService, "get_service_response", return_value=[])
async def test_when_sending_the_right_params_to_earnings_router_then_return_empty_list(
    mock_get_service_response,
):

    response = await ExchangeRouter.get_br_earnings(
        earnings=GetEarningsModel(
            **{"symbol": "VALE3", "limit": 1, "offset": 0, "timestamp": 1234566857}
        )
    )

    assert response == []


@pytest.mark.asyncio
async def test_when_sending_wrong_params_to_earnings_router_then_raise_validation_error():

    with pytest.raises(ValidationError):
        await ExchangeRouter.get_br_earnings(
            earnings=GetEarningsModel(
                **{"symbol": None, "limit": 1, "offset": 0, "timestamp": None}
            )
        )


# client earnings router
earnings_response_stub = {"payable_earnings": [10000.0, 25000.0], "record_date_earnings": [20000.0]}

@pytest.mark.asyncio
@patch.object(JwtService, 'get_thebes_answer_from_request', return_value=payload_data_dummy)
@patch.object(EarningsFromClient, 'get_service_response', return_value=earnings_response_stub)
async def test_when_sending_right_params_then_return_the_expected_values(
        mock_get_thebes_answer_from_request, mock_get_service_response):
    response = await ExchangeRouter.get_earnings_from_client(
        request=MagicMock(scope=scope_stub_2, headers=MagicMock(raw=x_thebes_tuple)),
        earnings_client=EarningsClientModel(
            **{
                "cod_client": 111,
                "region": Region.BR.value,
                "limit": 2,
                "offset": 0,
            }
        ),
    )
    assert response == earnings_response_stub


@pytest.mark.asyncio
async def test_when_sending_wrong_params_to_earnings_client_router_then_raise_validation_error():

    with pytest.raises(ValidationError):
        await ExchangeRouter.get_earnings_from_client(
            earnings_client=EarningsClientModel(
                **{
                    "cod_client": None,
                    "region": None,
                    "limit": 2,
                    "offset": 0,
                }
            )
        )


@pytest.mark.asyncio
async def test_when_sending_the_wrong_payload_jwt_invalid_to_earnings_client_router_then_raise_unauthorized_error():

    with pytest.raises(UnauthorizedError):
        await ExchangeRouter.get_earnings_from_client(
            request=MagicMock(scope=scope_stub),
            earnings_client=EarningsClientModel(
                **{
                "cod_client": 111,
                "region": Region.BR.value,
                "limit": 2,
                "offset": 0,
            }
            ),
        )
