# Standard Libs
import pytest
from unittest.mock import patch, MagicMock
from unittest import mock


# Internal Libs
from api.services.get_statement.get_statement import GetStatement
from api.services.statement.service import Statement
from tests.stubs.project_stubs.stub_data import (payload_data_dummy,
                                                 user_jwt_dummy, portfolios_jwt_dummy, StubOracleRepository)
from tests.stubs.project_stubs.stub_get_statement import (statement_dummy_request,
                                                          dummy_statement_response_br,
                                                          statement_another_dummy_request,
                                                          query_dummy)


@pytest.mark.asyncio
@patch('api.services.get_statement.get_statement.GetStatement.get_service_response',
       return_value=dummy_statement_response_br)
async def test_when_jwt_and_params_are_valid_then_return_the_expected_response(mock_get_service_response):
    statement_response = await GetStatement.get_service_response(jwt_data=payload_data_dummy,
                                                                 statement=statement_dummy_request)
    assert statement_response == dummy_statement_response_br
    assert statement_response.get('balance') == 987654.3
    assert statement_response.get('statements')[0]['value'] == -23456.98
    assert isinstance(statement_response, dict)


@pytest.mark.asyncio
@patch('api.services.get_statement.get_statement.GetStatement.get_service_response',
       return_value={})
async def test_when_region_and_timestamp_are_invalid_then_return_an_empty_dict_which_is_the_expected_value(
        mock_get_service_response):
    statement_response = await GetStatement.get_service_response(jwt_data=payload_data_dummy,
                                                                 statement=statement_another_dummy_request)
    assert statement_response == {}
    mock_get_service_response.assert_called_once()


@pytest.mark.asyncio
@patch.object(GetStatement, 'get_service_response', return_value=Exception)
async def test_when_invalid_jwt_is_sent_then_return_the_expected_which_is_an_exception(mock_get_service_response):
    jwt_data_dummy = ""
    statement_response = await GetStatement.get_service_response(jwt_data=jwt_data_dummy,
                                                                 statement=statement_dummy_request)
    assert statement_response == Exception


@pytest.mark.asyncio
@patch.object(GetStatement, 'get_service_response', return_value=Exception)
async def test_when_either_jwt_and_statement_params_arent_sent_then_return_exception(mock_get_service_response):
    jwt_data_dummy = ""
    invalid_statement_dummy = ""
    statement_response = await GetStatement.get_service_response(jwt_data=jwt_data_dummy,
                                                                 statement=invalid_statement_dummy)
    assert statement_response == Exception


@pytest.mark.asyncio
@patch.object(GetStatement, "get_service_response", return_value=dummy_statement_response_br)
async def test_when_jwt_data_payload_is_valid_then_check_if_the_user_is_in_the_payload_response(
        mock_get_service_response):
    response = await GetStatement.get_service_response(statement=statement_dummy_request,
                                                       jwt_data=payload_data_dummy)
    jwt = payload_data_dummy.get("user")
    assert response is not None
    assert jwt == user_jwt_dummy
    assert isinstance(jwt, dict)
    mock_get_service_response.assert_called()


@pytest.mark.asyncio
@patch.object(GetStatement, "get_service_response", return_value=dummy_statement_response_br)
async def test_when_jwt_data_payload_is_valid_then_check_if_portfolios_is_in_the_payload_response(
        mock_get_service_response):
    response = await GetStatement.get_service_response(statement=statement_dummy_request,
                                                       jwt_data=payload_data_dummy)
    jwt = payload_data_dummy["user"]["portfolios"]
    assert response is not None
    assert jwt == portfolios_jwt_dummy
    assert isinstance(jwt, dict)
    mock_get_service_response.assert_called()


@pytest.mark.asyncio
@mock.patch.object(Statement, "get_dw_statement", return_value={"balance": 1646794800.0})
async def test_when_dw_statement_function_us_then_return_expected_which_is_the_statement_as_response(
        mock_get_dw_statement):
    statement_response = await Statement.get_dw_statement(
        start_date=1646757399000, end_date=1648485399000, offset=1, limit=1)
    assert 'balance' in statement_response
    assert statement_response['balance'] == 1646794800.0
    mock_get_dw_statement.assert_called()


@pytest.mark.asyncio
@mock.patch.object(Statement, "get_dw_statement", return_value={})
async def test_when_dw_the_params_are_not_valid_then_return_an_empty_dict_as_expected(mock_get_dw_statement):
    statement_response = await Statement.get_dw_statement(
        start_date=0, end_date=0, offset=1, limit=1)
    assert statement_response == {}
    mock_get_dw_statement.assert_called()


@pytest.mark.asyncio
@patch('api.repositories.base_repositories.oracle.repository.OracleBaseRepository.get_data', return_value=10000.41)
async def test_when_sending_a_valid_query_then_return_expected_value(mock_get_data):
    query_dummy_request = query_dummy
    GetStatement.oracle_singleton_instance = StubOracleRepository
    response = GetStatement.oracle_singleton_instance.get_data(sql=query_dummy_request)
    assert response == 10000.41


@pytest.mark.asyncio
@patch('api.repositories.base_repositories.oracle.repository.OracleBaseRepository.get_data', return_value={})
async def test_when_sending_an_invalid_query_then_return_an_empty_dict_expected(mock_get_data):
    invalid_query_dummy = None
    GetStatement.oracle_singleton_instance = StubOracleRepository
    response = GetStatement.oracle_singleton_instance.get_data(sql=invalid_query_dummy)
    assert response == {}
