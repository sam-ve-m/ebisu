# Standard Libs
import pytest
from unittest.mock import patch, MagicMock
from pydantic import ValidationError

# INTERNAL LIBS
from api.domain.enums.region import Region
from api.domain.validators.exchange_info.client_orders_validator import GetClientOrderModel
from api.domain.validators.exchange_info.earnings_validator import GetEarningsModel
from api.domain.validators.exchange_info.get_balance_validator import GetBalanceModel
from api.domain.validators.exchange_info.get_statement_validator import GetStatementModel
from api.domain.validators.exchange_info.list_broker_note_validator import BrokerNoteRegion, BrokerNoteMarket, \
    ListBrokerNoteModel
from api.domain.validators.exchange_info.list_client_order_validator import ListClientOrderModel
from api.routers.exchange_informations.router import ExchangeRouter
from api.services.get_balance.get_balance import GetBalance
from api.exceptions.exceptions import UnauthorizedError
from api.services.get_client_orders.get_client_orders import GetOrders
from api.services.get_earnings.get_client_earnings import EarningsService
from api.services.get_statement.get_statement import GetStatement
from api.services.list_broker_note.list_broker_note import ListBrokerNote
from api.services.list_client_orders.list_client_orders import ListOrders
from api.services.request_statement.request_statement import RequestStatement
from tests.api.stubs.project_stubs.stub_earnings import earnings_dummy_response
from tests.api.stubs.project_stubs.stub_get_client_orders import client_order_response_dummy
from tests.api.stubs.project_stubs.stub_get_statement import dummy_bank_statement_response, statement_valid_params
from tests.api.stubs.project_stubs.stub_list_client_orders import stub_expected_response
from tests.api.stubs.project_stubs.stub_request_statement_pdf import bank_statement_pdf_br_dummy, file_link_stub

# STUBS
balance_stub = {'payload': {'balance': 49030153.7}}
scope_stub = {'type': 'http', 'headers': {'x-thebes-answer': None}}
scope_stub_2 = {'type': 'http', 'headers': {'x-thebes-answer': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJleHAiOiAxNjc4MjA5Nzg4LCAiY3JlYXRlZF9hdCI6IDE2NDY2NzM3ODguNDQyMTM5LCAic2NvcGUiOiB7InZpZXdfdHlwZSI6ICJkZWZhdWx0IiwgInVzZXJfbGV2ZWwiOiAiY2xpZW50IiwgImZlYXR1cmVzIjogWyJkZWZhdWx0IiwgInJlYWx0aW1lIl19LCAidXNlciI6IHsidW5pcXVlX2lkIjogIjQwZGI3ZmVlLTZkNjAtNGQ3My04MjRmLTFiZjg3ZWRjNDQ5MSIsICJuaWNrX25hbWUiOiAiUkFTVDMiLCAicG9ydGZvbGlvcyI6IHsiYnIiOiB7ImJvdmVzcGFfYWNjb3VudCI6ICIwMDAwMDAwMTQtNiIsICJibWZfYWNjb3VudCI6ICIxNCJ9LCAidXMiOiB7Il8iOiBudWxsfX0sICJjbGllbnRfaGFzX2JyX3RyYWRlX2FsbG93ZWQiOiBmYWxzZSwgImNsaWVudF9oYXNfdXNfdHJhZGVfYWxsb3dlZCI6IGZhbHNlLCAiY2xpZW50X3Byb2ZpbGUiOiAiaW52ZXN0b3IifX0.ccXheG6ORUWlsOmp0iZnyx39aEgW9zIEtL9Tf3aZ4bXXz_pIwI9f8LW15MHYjyvrkCjjb6dEuxQSqwxbYQvPdwq2PTJ0kLROYnDx8v0z9CX6WYHiLDapWHRoosgGUU20x1hqD_k_GSvpw_7DEyKkXavAJtK7XvwnZToFyWb1F1UhTVFsr_Oybh2PDsi6NvVgd3fhs17GVI81DmWFcBfz4J01S_446P-xmgfHjlOTatCKR1_0I2oDKeLi2fH160xXfApqfT5nOq9vsui-WaoI87_noUc3CQXk2BvqfFu83TRk2sIj4xKZp633DtCyM8D6iJngNPclH-K6o23EwSSa1g'}}
x_thebes_tuple = [(b'x-thebes-answer', b'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJleHAiOiAxNjc4MjA5Nzg4LCAiY3JlYXRlZF9hdCI6IDE2NDY2NzM3ODguNDQyMTM5LCAic2NvcGUiOiB7InZpZXdfdHlwZSI6ICJkZWZhdWx0IiwgInVzZXJfbGV2ZWwiOiAiY2xpZW50IiwgImZlYXR1cmVzIjogWyJkZWZhdWx0IiwgInJlYWx0aW1lIl19LCAidXNlciI6IHsidW5pcXVlX2lkIjogIjQwZGI3ZmVlLTZkNjAtNGQ3My04MjRmLTFiZjg3ZWRjNDQ5MSIsICJuaWNrX25hbWUiOiAiUkFTVDMiLCAicG9ydGZvbGlvcyI6IHsiYnIiOiB7ImJvdmVzcGFfYWNjb3VudCI6ICIwMDAwMDAwMTQtNiIsICJibWZfYWNjb3VudCI6ICIxNCJ9LCAidXMiOiB7Il8iOiBudWxsfX0sICJjbGllbnRfaGFzX2JyX3RyYWRlX2FsbG93ZWQiOiBmYWxzZSwgImNsaWVudF9oYXNfdXNfdHJhZGVfYWxsb3dlZCI6IGZhbHNlLCAiY2xpZW50X3Byb2ZpbGUiOiAiaW52ZXN0b3IifX0.ccXheG6ORUWlsOmp0iZnyx39aEgW9zIEtL9Tf3aZ4bXXz_pIwI9f8LW15MHYjyvrkCjjb6dEuxQSqwxbYQvPdwq2PTJ0kLROYnDx8v0z9CX6WYHiLDapWHRoosgGUU20x1hqD_k_GSvpw_7DEyKkXavAJtK7XvwnZToFyWb1F1UhTVFsr_Oybh2PDsi6NvVgd3fhs17GVI81DmWFcBfz4J01S_446P-xmgfHjlOTatCKR1_0I2oDKeLi2fH160xXfApqfT5nOq9vsui-WaoI87_noUc3CQXk2BvqfFu83TRk2sIj4xKZp633DtCyM8D6iJngNPclH-K6o23EwSSa1g')]
list_broker_note_stub = [{"market": "bmf", "region": "BR", "day": 5,
        "broker_note_link": "https://brokerage-note-and-bank-statement.s3.amazonaws.com/14/BR/broker_note/2022/4/5.pdf?AWS"}]
statement_stub = {"balance": 10000.2, "statements": [1035546, 3000, 20000]}


# get balance router
@pytest.mark.asyncio
@patch.object(GetBalance, 'get_service_response', return_value=balance_stub)
async def test_when_sending_the_right_params_to_get_balance_then_return_the_expected(
        mock_get_service_response
):

    response = await ExchangeRouter.get_balance(
        request=MagicMock(scope=scope_stub_2, headers=MagicMock(raw=x_thebes_tuple)),
        balance=GetBalanceModel(**{"region": 'BR'}))

    assert response == balance_stub
    assert 'payload' in response
    assert response.get('payload').get('balance') == 49030153.7
    assert isinstance(response, dict)


@pytest.mark.asyncio
@patch.object(GetBalance, 'get_service_response', return_value={"payload": {}})
async def test_when_sending_the_right_params_to_get_balance_then_return_an_empty_list_as_expected(
        mock_get_service_response
):

    response = await ExchangeRouter.get_balance(
        request=MagicMock(scope=scope_stub_2, headers=MagicMock(raw=x_thebes_tuple)),
        balance=GetBalanceModel(**{"region": 'BR'}))

    assert 'payload' in response
    assert response.get('payload') == {}
    assert isinstance(response, dict)


@pytest.mark.asyncio
async def test_when_sending_wrong_params_of_region_to_get_balance_then_raise_validation_error():

    with pytest.raises(ValidationError):
        await ExchangeRouter.get_balance(
            request=MagicMock(scope=scope_stub_2, headers=MagicMock(raw=x_thebes_tuple)),
            balance=GetBalanceModel(**{"region": None}))


@pytest.mark.asyncio
async def test_when_sending_the_wrong_payload_jwt_invalid_to_get_balance_then_raise_unauthorized_error():

    with pytest.raises(UnauthorizedError):
        await ExchangeRouter.get_balance(request=MagicMock(scope=scope_stub),
                                         balance=GetBalanceModel(**{"region": 'BR'}))


# list broker note router
@pytest.mark.asyncio
@patch.object(ListBrokerNote, 'get_service_response', return_value=list_broker_note_stub)
async def test_when_sending_the_right_params_to_get_list_broker_note_then_return_the_expected(
        mock_get_service_response
):
    link_response_stub = 'https://brokerage-note-and-bank-statement.s3.amazonaws.com/14/BR/broker_note/2022/4/5.pdf?AWS'

    response = await ExchangeRouter.get_broker_note(
        request=MagicMock(scope=scope_stub_2,
                          headers=MagicMock(
                              raw=x_thebes_tuple)),
        broker_note=ListBrokerNoteModel(**{"region": BrokerNoteRegion.BR.value,
                                           "market": BrokerNoteMarket.BMF.value,
                                           "year": 2022,
                                           "month": 4}))
    assert response == list_broker_note_stub
    assert response[0].get('broker_note_link') == link_response_stub


@pytest.mark.asyncio
@patch.object(ListBrokerNote, 'get_service_response', return_value=[])
async def test_when_sending_the_right_params_to_get_list_broker_note_then_return_the_an_empty_list(
        mock_get_service_response
):
    list_broker_response = await ExchangeRouter.get_broker_note(
        request=MagicMock(scope=scope_stub_2,
                          headers=MagicMock(
                              raw=x_thebes_tuple)),
        broker_note=ListBrokerNoteModel(**{"region": BrokerNoteRegion.BR.value,
                                           "market": BrokerNoteMarket.BOVESPA.value,
                                           "year": 2018,
                                           "month": 1}))
    assert list_broker_response == []
    assert isinstance(list_broker_response, list)


@pytest.mark.asyncio
async def test_when_sending_wrong_params_of_list_broker_note_model_to_get_broker_note_then_raise_validation_error():

    with pytest.raises(ValidationError):
        await ExchangeRouter.get_broker_note(
        request=MagicMock(scope=scope_stub_2,
                          headers=MagicMock(
                              raw=x_thebes_tuple)),
        broker_note=ListBrokerNoteModel(**{"region": None,
                                           "market": None,
                                           "year": 2018,
                                           "month": 1}))


@pytest.mark.asyncio
async def test_when_sending_the_wrong_payload_jwt_invalid_to_broker_note_router_then_raise_unauthorized_error():

    with pytest.raises(UnauthorizedError):
        await ExchangeRouter.get_broker_note(
            request=MagicMock(scope=scope_stub),
            broker_note=ListBrokerNoteModel(**{"region": BrokerNoteRegion.BR.value,
                                           "market": BrokerNoteMarket.BOVESPA.value,
                                           "year": 2018,
                                           "month": 1}))


# request bank statement pdf router
@pytest.mark.asyncio
@patch.object(RequestStatement, 'get_service_response', return_value=bank_statement_pdf_br_dummy)
async def test_when_sending_the_right_params_to_request_bank_statement_pdf_then_return_the_expected(
        mock_get_service_response
):
    response_statement = await ExchangeRouter.get_request_bank_statement(
        request=MagicMock(scope=scope_stub_2,
                          headers=MagicMock(
                              raw=x_thebes_tuple)),
        region=Region.BR.value,
        start_date=1646757399000,
        end_date=1648485399000)

    assert response_statement == bank_statement_pdf_br_dummy
    assert response_statement.get('pdf_link') == file_link_stub


@pytest.mark.asyncio
async def test_when_sending_wrong_params_of_request_statement_model_then_raise_validation_error():

    with pytest.raises(TypeError):
        response = await ExchangeRouter.get_request_bank_statement(
        request=MagicMock(scope=scope_stub_2,
                          headers=MagicMock(
                              raw=x_thebes_tuple)),
        region="",
        start_date=None,
        end_date=None)

        assert response == "unsupported operand type(s) for /: 'NoneType' and 'int'"


@pytest.mark.asyncio
async def test_when_sending_the_wrong_payload_jwt_invalid_to_request_statement_router_then_raise_unauthorized_error():

    with pytest.raises(UnauthorizedError):
        await ExchangeRouter.get_request_bank_statement(
        request=MagicMock(scope=scope_stub_2),
        region=Region.BR.value,
        start_date=1646757399000,
        end_date=1648485399000)


# bank statement router
@pytest.mark.asyncio
@patch.object(GetStatement, 'get_service_response', return_value=statement_stub)
async def test_when_sending_the_right_params_to_bank_statement_then_return_the_expected(
        mock_get_service_response
):
    response_statement = await ExchangeRouter.get_bank_statement(
        request=MagicMock(scope=scope_stub_2,
                          headers=MagicMock(
                              raw=x_thebes_tuple)),
        statement=GetStatementModel(**{"region": BrokerNoteRegion.BR.value,
                                        "limit": 1,
                                       "offset": 0,
                                        "start_date": 1646757399000,
                                        "end_date": 1648485399000}))

    assert response_statement == statement_stub


@pytest.mark.asyncio
async def test_when_sending_wrong_params_of_get_statement_model_then_raise_validation_error():

    with pytest.raises(ValidationError):
        await ExchangeRouter.get_bank_statement(
            request=MagicMock(scope=scope_stub_2,
                              headers=MagicMock(
                                  raw=x_thebes_tuple)),
            statement=GetStatementModel(**{"region": None,
                                           "limit": 1,
                                           "offset": 0,
                                           "start_date": None,
                                           "end_date": None}))


@pytest.mark.asyncio
async def test_when_sending_the_wrong_payload_jwt_invalid_to_get_statement_router_then_raise_unauthorized_error():

    with pytest.raises(UnauthorizedError):
        await ExchangeRouter.get_bank_statement(
            request=MagicMock(scope=scope_stub_2),
            statement=GetStatementModel(**{"region": BrokerNoteRegion.BR.value,
                                           "limit": 1,
                                           "offset": 0,
                                           "start_date": 1646757399000,
                                           "end_date": 1648485399000}))


#get client orders router
@pytest.mark.asyncio
@patch.object(GetOrders, 'get_service_response', return_value=client_order_response_dummy)
async def test_when_sending_the_right_params_to_client_order_router_then_return_the_expected(
        mock_get_service_response
):

    response = await ExchangeRouter.get_client_orders(
        request=MagicMock(scope=scope_stub_2,
                          headers=MagicMock(
                              raw=x_thebes_tuple)),
        client_order=GetClientOrderModel(**{"region": Region.BR.value,
                                            "cl_order_id": "008cf873-ee2a-4b08-b277-74b8b17f6e64"}))

    assert response == client_order_response_dummy
    assert response.get('symbol') == "VALE3"


@pytest.mark.asyncio
async def test_when_sending_wrong_params_to_get_client_orders_router_then_raise_validation_error():

    with pytest.raises(ValidationError):
        await ExchangeRouter.get_client_orders(
            request=MagicMock(scope=scope_stub_2,
                              headers=MagicMock(
                                  raw=x_thebes_tuple)),
            client_order=GetClientOrderModel(**{"region": None,
                                            "cl_order_id": None}))


@pytest.mark.asyncio
async def test_when_sending_the_wrong_payload_jwt_invalid_to_get_client_orders_router_then_raise_unauthorized_error():

    with pytest.raises(UnauthorizedError):
        await ExchangeRouter.get_client_orders(
            request=MagicMock(scope=scope_stub_2),
            client_order=GetClientOrderModel(**{"region": Region.BR.value,
                                                "cl_order_id": "008cf873-ee2a-4b08-b277-74b8b17f6e64"}))


# list client orders router
@pytest.mark.asyncio
@patch.object(ListOrders, 'get_service_response', return_value=stub_expected_response)
async def test_when_sending_the_right_params_to_list_client_order_router_then_return_the_expected(
        mock_get_service_response
):

    response = await ExchangeRouter.list_client_orders(
        request=MagicMock(scope=scope_stub_2,
                          headers=MagicMock(
                              raw=x_thebes_tuple)),
        list_client_orders=ListClientOrderModel(**{"region": Region.BR.value,
                                                    "limit": 1,
                                                    "offset": 0,
                                                    "order_status": "FILLED"}))

    assert response == stub_expected_response
    assert response[0].get('name') == 'CannaPharmaRx Inc'


@pytest.mark.asyncio
async def test_when_sending_wrong_params_to_list_client_orders_router_then_raise_validation_error():

    with pytest.raises(ValidationError):
        await ExchangeRouter.list_client_orders(
            request=MagicMock(scope=scope_stub_2,
                              headers=MagicMock(
                                  raw=x_thebes_tuple)),
            list_client_orders=ListClientOrderModel(**{"region": None,
                                                       "limit": 1,
                                                       "offset": 0,
                                                       "order_status": None}))


@pytest.mark.asyncio
async def test_when_sending_the_wrong_payload_jwt_invalid_to_list_client_orders_router_then_raise_unauthorized_error():

    with pytest.raises(UnauthorizedError):
        await ExchangeRouter.list_client_orders(
            request=MagicMock(scope=scope_stub_2),
            list_client_orders=ListClientOrderModel(**{"region": Region.BR.value,
                                                    "limit": 1,
                                                    "offset": 0,
                                                    "order_status": "FILLED"}))


# earnings router
@pytest.mark.asyncio
@patch.object(EarningsService, 'get_service_response', return_value=earnings_dummy_response)
async def test_when_sending_the_right_params_to_earnings_router_then_return_the_expected(
        mock_get_service_response
):

    response = await ExchangeRouter.get_br_earnings(
        earnings=GetEarningsModel(**{"symbol": "PETR4",
                                                    "limit": 1,
                                                    "offset": 0,
                                                    "timestamp": 1646757399000}))

    assert response == earnings_dummy_response
    assert response[0].get('price') == 299


@pytest.mark.asyncio
@patch.object(EarningsService, 'get_service_response', return_value=[])
async def test_when_sending_the_right_params_to_earnings_router_then_return_empty_list(
        mock_get_service_response
):

    response = await ExchangeRouter.get_br_earnings(
        earnings=GetEarningsModel(**{"symbol": "VALE3",
                                    "limit": 1,
                                    "offset": 0,
                                    "timestamp": 1234566857}))

    assert response == []


@pytest.mark.asyncio
async def test_when_sending_wrong_params_to_earnings_router_then_raise_validation_error():

    with pytest.raises(ValidationError):
        await ExchangeRouter.get_br_earnings(
            earnings=GetEarningsModel(**{"symbol": None,
                                         "limit": 1,
                                         "offset": 0,
                                         "timestamp": None}))
