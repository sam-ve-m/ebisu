from src.domain.exceptions.repository.exception import CustomerExchangeDataNotFound
from src.domain.exceptions.service.forex_exchange.exception import (
    InvalidToken, ExpiredToken, DroppedToken, CaronteCantFindToken, UnexpectedErrorWhenTryingToGetExchangeSimulationProposal,
    CustomerQuotationTokenNotFound
)

from src.services.forex_exchange.proposal_simulation.service import CustomerExchangeService
from .stubs import (
    stub_currency_exchange, stub_customer_exchange_data, stub_caronte_response_success, stub_caronte_response_forbidden,
    stub_caronte_response_bad_request, stub_customer_exchange_request_model, stub_config_path, stub_config_path,
    stub_caronte_response_token_not_found, stub_caronte_response_unauthorized, stub_caronte_response_unexpected_error
)

# Standards
from unittest.mock import patch

# Third party
import pytest


@pytest.mark.asyncio
@patch("src.services.forex_exchange.proposal_simulation.service.UserRepository.get_user_exchange_data", return_value=stub_customer_exchange_data)
async def test_when_customer_have_exchange_data_then_return_expected_values(mock_user_repository):
    result = await CustomerExchangeService._CustomerExchangeService__get_customer_exchange_account_data(
        exchange_account_id=12345,
        currency_exchange=stub_currency_exchange
    )
    assert isinstance(result, dict)
    assert result.get("exchange_account_id") == 12345


@pytest.mark.asyncio
@patch("src.services.forex_exchange.proposal_simulation.service.UserRepository.get_user_exchange_data", return_value=None)
async def test_when_customer_not_have_exchange_data_then_raises(mock_user_repository):
    with pytest.raises(CustomerExchangeDataNotFound):
        await CustomerExchangeService._CustomerExchangeService__get_customer_exchange_account_data(
            exchange_account_id=12345,
            currency_exchange=stub_currency_exchange
        )


@pytest.mark.asyncio
@patch("src.domain.models.forex_exchange.customer_exchange_request_data.model.config", side_effect=stub_config_path)
@patch("src.services.forex_exchange.proposal_simulation.service.ExchangeCompanyApi.request_as_client",
       return_value=stub_caronte_response_success)
async def test_when_get_customer_token_with_successfully_then_return_token_data(mock_request_caronte, mock_config):
    result = await CustomerExchangeService._CustomerExchangeService__get_customer_token_on_route_21(
        customer_exchange_request_model=stub_customer_exchange_request_model
    )

    assert isinstance(result, dict)


@pytest.mark.asyncio
@patch("src.domain.models.forex_exchange.customer_exchange_request_data.model.config", side_effect=stub_config_path)
@patch("src.services.forex_exchange.proposal_simulation.service.ExchangeCompanyApi.request_as_client",
       return_value=stub_caronte_response_bad_request)
async def test_when_get_customer_token_result_is_bad_request_then_raises(mock_request_caronte, mock_config):
    with pytest.raises(ExpiredToken):
        await CustomerExchangeService._CustomerExchangeService__get_customer_token_on_route_21(
            customer_exchange_request_model=stub_customer_exchange_request_model
        )


@pytest.mark.asyncio
@patch("src.domain.models.forex_exchange.customer_exchange_request_data.model.config", side_effect=stub_config_path)
@patch("src.services.forex_exchange.proposal_simulation.service.ExchangeCompanyApi.request_as_client",
       return_value=stub_caronte_response_unauthorized)
async def test_when_get_customer_token_result_is_unauthorized_then_raises(mock_request_caronte, mock_config):
    with pytest.raises(InvalidToken):
        await CustomerExchangeService._CustomerExchangeService__get_customer_token_on_route_21(
            customer_exchange_request_model=stub_customer_exchange_request_model
        )


@pytest.mark.asyncio
@patch("src.domain.models.forex_exchange.customer_exchange_request_data.model.config", side_effect=stub_config_path)
@patch("src.services.forex_exchange.proposal_simulation.service.ExchangeCompanyApi.request_as_client",
       return_value=stub_caronte_response_forbidden)
async def test_when_get_customer_token_result_is_forbidden_then_raises(mock_request_caronte, mock_config):
    with pytest.raises(DroppedToken):
        await CustomerExchangeService._CustomerExchangeService__get_customer_token_on_route_21(
            customer_exchange_request_model=stub_customer_exchange_request_model
        )


@pytest.mark.asyncio
@patch("src.domain.models.forex_exchange.customer_exchange_request_data.model.config", side_effect=stub_config_path)
@patch("src.services.forex_exchange.proposal_simulation.service.ExchangeCompanyApi.request_as_client",
       return_value=stub_caronte_response_token_not_found)
async def test_when_get_customer_token_result_is_token_not_found_then_raises(mock_request_caronte, mock_config):
    with pytest.raises(CaronteCantFindToken):
        await CustomerExchangeService._CustomerExchangeService__get_customer_token_on_route_21(
            customer_exchange_request_model=stub_customer_exchange_request_model
        )


@pytest.mark.asyncio
@patch("src.domain.models.forex_exchange.customer_exchange_request_data.model.config", side_effect=stub_config_path)
@patch("src.services.forex_exchange.proposal_simulation.service.ExchangeCompanyApi.request_as_client",
       return_value=stub_caronte_response_unexpected_error)
async def test_when_get_customer_token_result_is_unexpected_error_found_then_raises(mock_request_caronte, mock_config):
    with pytest.raises(UnexpectedErrorWhenTryingToGetExchangeSimulationProposal):
        await CustomerExchangeService._CustomerExchangeService__get_customer_token_on_route_21(
            customer_exchange_request_model=stub_customer_exchange_request_model
        )

