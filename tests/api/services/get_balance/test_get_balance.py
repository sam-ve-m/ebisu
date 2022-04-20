import pytest
from unittest.mock import patch
from tests.stubs.jwt_data.stub_jwt import (payload_data_stub,
                                           balance_response_stub_br,
                                           balance_response_stub_us,
                                           balance_payload_stub_br,
                                           balance_payload_stub_us,
                                           user_jwt_stub,
                                           portfolios_jwt_stub)

from api.services.get_balance.get_balance import GetBalance
from api.services.statement.service import Statement


@pytest.mark.asyncio
@patch.object(GetBalance, "get_service_response", return_value={})
async def test_when_balance_br_return_value_is_none_then_return_empty_dict(mock_get_service_response):
    response = await GetBalance.get_service_response(balance=balance_response_stub_br,
                                                     jwt_data=payload_data_stub)
    assert response == {}
    mock_get_service_response.assert_called()


@pytest.mark.asyncio
@patch.object(GetBalance, "get_service_response", return_value={})
async def test_when_balance_br_return_value_is_none_then_return_empty_dict(mock_get_service_response):
    balance_data = None
    response = await GetBalance.get_service_response(balance=balance_data,
                                                     jwt_data=payload_data_stub)
    assert response == {}
    mock_get_service_response.assert_called()


@pytest.mark.asyncio
@patch.object(GetBalance, "get_service_response", return_value=balance_payload_stub_br)
async def test_when_balance_return_value_is_valid_then_return_the_expected(mock_get_service_response):
    response = await GetBalance.get_service_response(balance=balance_response_stub_br,
                                                     jwt_data=payload_data_stub)
    assert 'payload' in response
    assert response == {'payload': {'balance': 47499394.54}}
    mock_get_service_response.assert_called()


@pytest.mark.asyncio
@patch.object(GetBalance, "get_service_response", return_value=Exception)
async def test_when_no_param_of_region_is_passed_then_raise_exception(mock_get_service_response):
    response = await GetBalance.get_service_response(balance={'region': None},
                                                     jwt_data=payload_data_stub)
    assert response == Exception
    mock_get_service_response.assert_called()


@pytest.mark.asyncio
@patch.object(GetBalance, "get_service_response", return_value=Exception)
async def test_when_no_param_of_region_is_passed_then_raise_exception(mock_get_service_response):
    response = await GetBalance.get_service_response(balance={'region': ""},
                                                     jwt_data=payload_data_stub)
    assert response == Exception
    mock_get_service_response.assert_called()


@pytest.mark.asyncio
@patch.object(GetBalance, "get_service_response", return_value=balance_payload_stub_us)
async def test_when_balance_us_return_value_is_valid_then_return_the_expected(mock_get_service_response):
    response = await GetBalance.get_service_response(balance=balance_payload_stub_us,
                                                     jwt_data=payload_data_stub)
    assert 'payload' in response
    assert response == {'payload': {'balance': 47499394.54}}
    mock_get_service_response.assert_called()


@pytest.mark.asyncio
@patch.object(GetBalance, "get_service_response", return_value={})
async def test_when_balance_us_return_value_is_none_then_return_empty_dict(mock_get_service_response):
    response = await GetBalance.get_service_response(balance=balance_response_stub_us,
                                                     jwt_data=payload_data_stub)
    assert response == {}


@pytest.mark.asyncio
@patch.object(Statement, "get_dw_balance", return_value=balance_payload_stub_us)
async def test_when_getting_balance_us_then_return_expected_and_payload_is_in_response(mock_get_dw_balance):
    response = await Statement.get_dw_balance()
    assert response is not None
    assert response == balance_payload_stub_us
    assert 'payload' in response


@pytest.mark.asyncio
@patch.object(GetBalance, "get_service_response", return_value=balance_payload_stub_br)
async def test_when_jwt_data_payload_is_valid_then_check_if_the_user_is_in_the_payload_response(
        mock_get_service_response):
    response = await GetBalance.get_service_response(balance=balance_response_stub_br,
                                                     jwt_data=payload_data_stub)
    jwt = payload_data_stub.get("user")
    assert response is not None
    assert jwt == user_jwt_stub
    assert isinstance(jwt, dict)
    mock_get_service_response.assert_called()


@pytest.mark.asyncio
@patch.object(GetBalance, "get_service_response", return_value=balance_payload_stub_br)
async def test_when_jwt_data_payload_is_valid_then_check_if_portfolios_is_in_the_payload_response(
        mock_get_service_response):
    response = await GetBalance.get_service_response(balance=balance_response_stub_br,
                                                     jwt_data=payload_data_stub)
    jwt = payload_data_stub["user"]["portfolios"]
    assert response is not None
    assert jwt == portfolios_jwt_stub
    assert isinstance(jwt, dict)
    mock_get_service_response.assert_called()
