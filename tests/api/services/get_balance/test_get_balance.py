# Standard Libs
import pytest
from unittest.mock import patch, MagicMock

# External Libs
from api.repositories.base_repositories.oracle.repository import OracleBaseRepository
from api.services.get_balance.get_balance import GetBalance
from api.services.statement.service import Statement
from tests.stubs.project_stubs.stub_data import (
                                                payload_data_dummy,
                                                StubOracleRepository)


@pytest.mark.asyncio
@patch.object(OracleBaseRepository, 'get_data', return_value="")
async def test_when_balance_br_return_value_is_none_then_return_empty_dict(mock_get_data):
    response = await GetBalance.get_service_response(balance=MagicMock(region=""),
                                                     jwt_data=payload_data_dummy)
    assert response == {}
    mock_get_data.assert_called()


@pytest.mark.asyncio
@patch.object(OracleBaseRepository, 'get_data', return_value=[{'VL_TOTAL': 10000.0}])
async def test_when_balance_return_value_is_valid_then_return_the_expected(mock_get_data):
    response = await GetBalance.get_service_response(balance=MagicMock(region="BR"),
                                                     jwt_data=payload_data_dummy)
    assert 'payload' in response
    assert response == {'payload': {'balance': 10000.0}}


@pytest.mark.asyncio
@patch.object(Statement, "get_dw_balance", return_value={"balance": 12000.0})
async def test_when_balance_us_return_value_is_valid_then_return_the_expected_value(mock_get_dw_balance):
    response = await GetBalance.get_service_response(balance=MagicMock(region="US"),
                                                     jwt_data=payload_data_dummy)
    assert response == {"balance": 12000.0}
    assert response.get('balance') == 12000.0


@pytest.mark.asyncio
@patch.object(Statement, "get_dw_balance", return_value={"balance": 104993635.20})
async def test_dw_balance_function_us_then_return_expected_and_balance_is_in_response(mock_get_dw_balance):
    response = await Statement.get_dw_balance()
    assert response == {"balance": 104993635.20}
    assert response['balance'] == 104993635.20
    assert isinstance(response, dict)


@pytest.mark.asyncio
async def test_when_sending_an_invalid_query_then_return_an_empty_dict_expected():
    query_dummy = None
    GetBalance.oracle_singleton_instance = StubOracleRepository
    response = GetBalance.oracle_singleton_instance.get_data(sql=query_dummy)
    assert response == {}


@pytest.mark.asyncio
async def test_when_sending_a_valid_query_then_return_expected_value():
    query_dummy = "SELECT VL_TOTAL FROM CORRWIN.TCCSALDO WHERE CD_CLIENTE = '49'"
    GetBalance.oracle_singleton_instance = StubOracleRepository
    response = GetBalance.oracle_singleton_instance.get_data(sql=query_dummy)
    assert response == 10000.41


@pytest.mark.asyncio
def test_balance_get_service_response_when_the_params_are_not_valid_then_raise_error_as_expected():
    balance_invalid_params = MagicMock(region=MagicMock(value=None),
                                          cl_order_id='008cf873-ee2a-4b08-b277-74b8b17f6e64')
    with pytest.raises(Exception) as err:
        GetBalance.get_service_response(jwt_data="", balance=balance_invalid_params)
        assert err == Exception


@pytest.mark.asyncio
def test_balance_get_service_response_when_the_statement_params_are_not_valid_then_raise_error_as_expected():
    with pytest.raises(Exception) as err:
        GetBalance.get_service_response(jwt_data=payload_data_dummy, balance="")
        assert err == Exception
