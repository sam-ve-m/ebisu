# Standard Libs
import pytest
from unittest.mock import patch
from unittest import mock

# Internal Libs
from api.services.get_statement.get_statement import GetStatement
from api.services.statement.service import Statement
from tests.stubs.project_stubs.stub_data import (payload_data_dummy,
                                                 StubOracleRepository)
from tests.stubs.project_stubs.stub_get_statement import (query_dummy,
                                                          dummy_bank_statement_response,
                                                          statement_params,
                                                          statement_valid_params,
                                                          statement_valid_params_us,
                                                          statement_invalid_params_us)


@pytest.mark.asyncio
@patch('api.services.get_statement.get_statement.GetStatement.oracle_singleton_instance.get_data',
       return_value=[{'VL_TOTAL': 10000.2}])
async def test_when_jwt_and_params_are_valid_then_return_the_expected_response(mock_get_data):
    statement_response = await GetStatement.get_service_response(jwt_data=payload_data_dummy,
                                                                 statement=statement_valid_params)
    assert statement_response == dummy_bank_statement_response
    assert statement_response.get('balance') == 10000.2
    assert statement_response.get('statements') == []
    assert isinstance(statement_response, dict)


@pytest.mark.asyncio
@patch('api.services.get_statement.get_statement.GetStatement.oracle_singleton_instance.get_data',
       return_value=[{'VL_TOTAL': None}])
async def test_when_region_and_timestamp_are_invalid_then_return_an_empty_dict_which_is_the_expected_value(
        mock_get_data):
    statement_response = await GetStatement.get_service_response(jwt_data=payload_data_dummy,
                                                                 statement=statement_params)
    assert statement_response == {'balance': None, 'statements': []}
    mock_get_data.assert_called()


@pytest.mark.asyncio
@mock.patch.object(Statement, "get_dw_statement", return_value={"balance": 48981636.93})
async def test_when_dw_statement_function_us_then_return_expected_which_is_the_statement_as_response(
        mock_get_dw_statement):
    statement_response = await GetStatement.get_service_response(jwt_data=payload_data_dummy,
                                                                 statement=statement_valid_params_us)
    assert 'balance' in statement_response
    assert statement_response['balance'] == 48981636.93


@pytest.mark.asyncio
async def test_when_sending_a_valid_query_then_return_expected_value():
    query_dummy_request = query_dummy
    GetStatement.oracle_singleton_instance = StubOracleRepository
    response = GetStatement.oracle_singleton_instance.get_data(sql=query_dummy_request)
    assert response == 10000.41


@pytest.mark.asyncio
async def test_when_sending_an_invalid_query_then_return_an_empty_dict_expected():
    invalid_query_dummy = None
    GetStatement.oracle_singleton_instance = StubOracleRepository
    response = GetStatement.oracle_singleton_instance.get_data(sql=invalid_query_dummy)
    assert response == {}


@pytest.mark.asyncio
async def test_get_service_response_when_the_params_are_not_valid_then_raise_error_as_expected():
    with pytest.raises(AttributeError) as err:
        await GetStatement.get_service_response(jwt_data="", statement=statement_invalid_params_us)
        assert err == "'str' object has no attribute 'get'"


@pytest.mark.asyncio
async def test_get_service_response_when_the_statement_params_are_not_valid_then_raise_error_as_expected():
    with pytest.raises(AttributeError) as err:
        await GetStatement.get_service_response(jwt_data=payload_data_dummy, statement="")
        assert err == "AttributeError: 'str' object has no attribute 'region'"
