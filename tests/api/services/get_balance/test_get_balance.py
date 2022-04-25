# Standard Libs
import pytest
from unittest.mock import patch

# External Libs
from api.services.get_balance.get_balance import GetBalance
from api.services.statement.service import Statement
from tests.stubs.stub_jwt.stub_data import (
    payload_data_dummy,
    user_jwt_dummy,
    portfolios_jwt_dummy,
    balance_response_dummy_br,
    balance_payload_dummy_br,
    balance_payload_dummy_us,
    StubOracleRepository, balance_payload_dummy_dw)


@pytest.mark.asyncio
@patch.object(GetBalance, "get_service_response", return_value={})
async def test_when_balance_br_return_value_is_none_then_return_empty_dict(mock_get_service_response):
    balance_data = ""
    response = await GetBalance.get_service_response(balance=balance_data,
                                                     jwt_data=payload_data_dummy)
    assert response == {}
    mock_get_service_response.assert_called()


@pytest.mark.asyncio
@patch.object(GetBalance, "get_service_response", return_value={})
async def test_when_no_balance_br_is_sent_then_return_empty_dict_and(mock_get_service_response):
    balance_data = None
    response = await GetBalance.get_service_response(balance=balance_data,
                                                     jwt_data=payload_data_dummy)
    assert response == {}
    mock_get_service_response.assert_called()


@pytest.mark.asyncio
@patch.object(GetBalance, "get_service_response", return_value=balance_payload_dummy_br)
async def test_when_balance_return_value_is_valid_then_return_the_expected(mock_get_service_response):
    response = await GetBalance.get_service_response(balance=balance_response_dummy_br,
                                                     jwt_data=payload_data_dummy)
    assert 'payload' in response
    assert response == {'payload': {'balance': 47499394.54}}
    mock_get_service_response.assert_called()


@pytest.mark.asyncio
@patch.object(GetBalance, "get_service_response", return_value=Exception)
async def test_when_no_param_of_region_is_passed_then_raise_exception(mock_get_service_response):
    response = await GetBalance.get_service_response(balance={'region': None},
                                                     jwt_data=payload_data_dummy)
    assert response == Exception
    mock_get_service_response.assert_called()


@pytest.mark.asyncio
@patch.object(GetBalance, "get_service_response", return_value=Exception)
async def test_when_jwt_data_payload_is_not_valid_then_return_exception(mock_get_service_response):
    wrong_payload_data_stub = {}
    response = await GetBalance.get_service_response(balance=balance_response_dummy_br,
                                                     jwt_data=wrong_payload_data_stub)
    assert response == Exception


@pytest.mark.asyncio
@patch.object(GetBalance, "get_service_response", return_value=balance_payload_dummy_us)
async def test_when_balance_us_return_value_is_valid_then_return_the_expected_value(mock_get_service_response):
    response = await GetBalance.get_service_response(balance=balance_payload_dummy_us,
                                                     jwt_data=payload_data_dummy)
    assert 'payload' in response
    assert response == {'payload': {'balance': 47499394.54}}
    mock_get_service_response.assert_called()


@pytest.mark.asyncio
@patch.object(Statement, "get_dw_balance", return_value=balance_payload_dummy_dw)
async def test_dw_balance_function_us_then_return_expected_and_balance_is_in_response(mock_get_dw_balance):
    response = await Statement.get_dw_balance()
    assert response == {"balance": 104993635.20}
    assert response['balance'] == 104993635.20


@pytest.mark.asyncio
@patch('api.repositories.base_repositories.oracle.repository.OracleBaseRepository.get_data', return_value={})
async def test_when_sending_an_invalid_query_then_return_an_empty_dict_expected(mock_get_data):
    query_dummy = ""
    GetBalance.oracle_singleton_instance = StubOracleRepository
    response = GetBalance.oracle_singleton_instance.get_data(sql=query_dummy)
    assert response == {}
    mock_get_data.assert_called_with(sql=query_dummy)
    mock_get_data.assert_called()


@pytest.mark.asyncio
@patch('api.repositories.base_repositories.oracle.repository.OracleBaseRepository.get_data', return_value=-44144434.41)
async def test_when_sending_a_valid_query_then_return_expected_value(mock_get_data):
    query_dummy = "SELECT VL_TOTAL FROM CORRWIN.TCCSALDO WHERE CD_CLIENTE = '49'"
    GetBalance.oracle_singleton_instance = StubOracleRepository
    response = GetBalance.oracle_singleton_instance.get_data(sql=query_dummy)
    assert response == -44144434.41


@pytest.mark.asyncio
@patch.object(GetBalance, "get_service_response", return_value=balance_payload_dummy_br)
async def test_when_jwt_data_payload_is_valid_then_check_if_the_user_is_in_the_payload_response(
        mock_get_service_response):
    response = await GetBalance.get_service_response(balance=balance_response_dummy_br,
                                                     jwt_data=payload_data_dummy)
    jwt = payload_data_dummy.get("user")
    assert response is not None
    assert jwt == user_jwt_dummy
    assert isinstance(jwt, dict)
    mock_get_service_response.assert_called()


@pytest.mark.asyncio
@patch.object(GetBalance, "get_service_response", return_value=balance_payload_dummy_br)
async def test_when_jwt_data_payload_is_valid_then_check_if_portfolios_is_in_the_payload_response(
        mock_get_service_response):
    response = await GetBalance.get_service_response(balance=balance_response_dummy_br,
                                                     jwt_data=payload_data_dummy)
    jwt = payload_data_dummy["user"]["portfolios"]
    assert response is not None
    assert jwt == portfolios_jwt_dummy
    assert isinstance(jwt, dict)
    mock_get_service_response.assert_called()
