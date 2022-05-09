# Standard Libs
import pytest
from unittest.mock import patch, MagicMock
from typing import List

# Internal Libs
from api.repositories.base_repositories.oracle.repository import OracleBaseRepository
from api.services.get_earnings.get_client_earnings import EarningsService
from api.services.get_earnings.strategies.br_earnings import GetBrEarnings
from tests.api.stubs.project_stubs.stub_data import StubOracleRepository
from tests.api.stubs.project_stubs.stub_earnings import (
                                                     earnings_dummy_br,
                                                     earnings_dummy_response,
                                                     normalize_earnings_dummy_request,
                                                     query_dummy_earnings)


@patch('api.services.get_earnings.get_client_earnings.EarningsService.normalize_earnings',
       return_value=earnings_dummy_response)
def test_when_a_request_of_normalization_is_sent_then_return_the_normalized_data(mock_normalize_earnings):
    normalized_response = EarningsService.normalize_earnings(client_earnings=normalize_earnings_dummy_request)
    assert normalized_response == earnings_dummy_response
    assert isinstance(normalized_response, List)
    mock_normalize_earnings.assert_called()


@pytest.mark.asyncio
@patch.object(EarningsService, 'get_service_response', return_value=earnings_dummy_response)
async def test_when_a_valid_request_is_sent_then_return_the_earnings_expected_response(mock_get_service_response):
    earnings_response = await EarningsService.get_service_response(earnings=earnings_dummy_br)
    assert earnings_response == earnings_dummy_response
    assert earnings_response[0]['symbol'] == "PETR4"
    assert earnings_response[0]['earnings_type'] is not None


@pytest.mark.asyncio
@patch.object(GetBrEarnings, 'build_query_earnings', return_value="")
@patch.object(OracleBaseRepository, 'get_data', return_value="")
@patch('api.services.get_earnings.get_client_earnings.earnings_regions')
async def test_when_invalid_request_is_sent_then_return_an_empty_object(mock_earnings_region,
                                                                        mock_build_query_earnings,
                                                                        mock_get_data):
    mock_earnings_region.__getitem__ = MagicMock(return_value=GetBrEarnings)
    earnings_response = await EarningsService.get_service_response(earnings=MagicMock(symbol="PETR4",
                                                                                      timestamp=1649611840000,
                                                                                      offset=0,
                                                                                      limit=1))
    assert earnings_response == []


@pytest.mark.asyncio
@patch('api.repositories.base_repositories.oracle.repository.OracleBaseRepository.get_data',
       return_value=10000.41)
async def test_when_sending_the_query_then_return_the_expected_value_of_earnings(mock_get_data):
    query_dummy = query_dummy_earnings
    EarningsService.oracle_earnings_singleton_instance = StubOracleRepository
    response = EarningsService.oracle_earnings_singleton_instance.get_data(sql=query_dummy)
    assert response == 10000.41


@pytest.mark.asyncio
@patch('api.repositories.base_repositories.oracle.repository.OracleBaseRepository.get_data',
       return_value={})
async def test_when_sending_an_invalid_query_then_return_the_expected_value(mock_get_data):
    query_dummy = None
    EarningsService.oracle_earnings_singleton_instance = StubOracleRepository
    response = EarningsService.oracle_earnings_singleton_instance.get_data(sql=query_dummy)
    assert response == {}
