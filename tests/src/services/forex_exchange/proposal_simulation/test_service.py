# Ebisu
from src.domain.exceptions.domain.forex.exception import (
    ErrorOnValidateExchangeSimulationProposalData,
)
from src.domain.exceptions.repository.forex.exception import CustomerForexDataNotFound
from src.domain.exceptions.service.forex.exception import (
    InvalidToken,
    ExpiredToken,
    DroppedToken,
    CaronteCantFindToken,
    UnexpectedErrorWhenTryingToGetExchangeSimulationProposal,
    CustomerQuotationTokenNotFound,
)

from src.services.forex.proposal_simulation.service import (
    CustomerExchangeService,
)

# Stubs
from .stubs import (
    stub_currency_exchange,
    stub_customer_exchange_data,
    stub_caronte_response_success_21,
    stub_caronte_response_forbidden,
    stub_caronte_response_bad_request,
    stub_customer_exchange_request_model,
    stub_config_path_quotation,
    stub_caronte_response_success_22,
    stub_caronte_response_token_not_found,
    stub_caronte_response_unauthorized,
    stub_caronte_response_unexpected_error,
    stub_config_path_exchange_simulation,
    stub_token_generated_in_route_21,
    stub_response_rote_21,
    stub_response_rote_22,
    stub_response_missing_data_rote_22,
)

# Standards
from unittest.mock import patch

# Third party
import pytest


@pytest.mark.asyncio
@patch(
    "src.services.forex.proposal_simulation.service.UserRepository.get_user_exchange_data",
    return_value=stub_customer_exchange_data,
)
async def test_when_customer_have_exchange_data_then_return_expected_values(
    mock_user_repository,
):
    result = await CustomerExchangeService._CustomerExchangeService__get_customer_exchange_account_data(
        exchange_account_id=12345, currency_exchange=stub_currency_exchange
    )
    assert isinstance(result, dict)
    assert result.get("exchange_account_id") == 12345


@pytest.mark.asyncio
@patch(
    "src.services.forex.proposal_simulation.service.UserRepository.get_user_exchange_data",
    return_value=None,
)
async def test_when_customer_not_have_exchange_data_then_raises(mock_user_repository):
    with pytest.raises(CustomerForexDataNotFound):
        await CustomerExchangeService._CustomerExchangeService__get_customer_exchange_account_data(
            exchange_account_id=12345, currency_exchange=stub_currency_exchange
        )


@pytest.mark.asyncio
@patch(
    "src.domain.models.forex.customer_exchange_request_data.model.config",
    side_effect=stub_config_path_quotation,
)
@patch(
    "src.services.forex.proposal_simulation.service.ExchangeCompanyApi.request_as_client",
    return_value=stub_caronte_response_success_21,
)
async def test_when_get_customer_token_with_successfully_then_return_token_data(
    mock_request_caronte, mock_config
):
    result = await CustomerExchangeService._CustomerExchangeService__get_customer_token_on_route_21(
        customer_exchange_request_model=stub_customer_exchange_request_model
    )

    assert isinstance(result, dict)


@pytest.mark.asyncio
@patch(
    "src.domain.models.forex.customer_exchange_request_data.model.config",
    side_effect=stub_config_path_quotation,
)
@patch(
    "src.services.forex.proposal_simulation.service.ExchangeCompanyApi.request_as_client",
    return_value=stub_caronte_response_bad_request,
)
async def test_when_get_customer_token_result_is_bad_request_then_raises(
    mock_request_caronte, mock_config
):
    with pytest.raises(ExpiredToken):
        await CustomerExchangeService._CustomerExchangeService__get_customer_token_on_route_21(
            customer_exchange_request_model=stub_customer_exchange_request_model
        )


@pytest.mark.asyncio
@patch(
    "src.domain.models.forex.customer_exchange_request_data.model.config",
    side_effect=stub_config_path_quotation,
)
@patch(
    "src.services.forex.proposal_simulation.service.ExchangeCompanyApi.request_as_client",
    return_value=stub_caronte_response_unauthorized,
)
async def test_when_get_customer_token_result_is_unauthorized_then_raises(
    mock_request_caronte, mock_config
):
    with pytest.raises(InvalidToken):
        await CustomerExchangeService._CustomerExchangeService__get_customer_token_on_route_21(
            customer_exchange_request_model=stub_customer_exchange_request_model
        )


@pytest.mark.asyncio
@patch(
    "src.domain.models.forex.customer_exchange_request_data.model.config",
    side_effect=stub_config_path_quotation,
)
@patch(
    "src.services.forex.proposal_simulation.service.ExchangeCompanyApi.request_as_client",
    return_value=stub_caronte_response_forbidden,
)
async def test_when_get_customer_token_result_is_forbidden_then_raises(
    mock_request_caronte, mock_config
):
    with pytest.raises(DroppedToken):
        await CustomerExchangeService._CustomerExchangeService__get_customer_token_on_route_21(
            customer_exchange_request_model=stub_customer_exchange_request_model
        )


@pytest.mark.asyncio
@patch(
    "src.domain.models.forex.customer_exchange_request_data.model.config",
    side_effect=stub_config_path_quotation,
)
@patch(
    "src.services.forex.proposal_simulation.service.ExchangeCompanyApi.request_as_client",
    return_value=stub_caronte_response_token_not_found,
)
async def test_when_get_customer_token_result_is_token_not_found_then_raises(
    mock_request_caronte, mock_config
):
    with pytest.raises(CaronteCantFindToken):
        await CustomerExchangeService._CustomerExchangeService__get_customer_token_on_route_21(
            customer_exchange_request_model=stub_customer_exchange_request_model
        )


@pytest.mark.asyncio
@patch(
    "src.domain.models.forex.customer_exchange_request_data.model.config",
    side_effect=stub_config_path_quotation,
)
@patch(
    "src.services.forex.proposal_simulation.service.ExchangeCompanyApi.request_as_client",
    return_value=stub_caronte_response_unexpected_error,
)
async def test_when_get_customer_token_result_is_unexpected_error_found_then_raises(
    mock_request_caronte, mock_config
):
    with pytest.raises(UnexpectedErrorWhenTryingToGetExchangeSimulationProposal):
        await CustomerExchangeService._CustomerExchangeService__get_customer_token_on_route_21(
            customer_exchange_request_model=stub_customer_exchange_request_model
        )


@pytest.mark.asyncio
@patch(
    "src.domain.models.forex.customer_exchange_request_data.model.config",
    side_effect=stub_config_path_exchange_simulation,
)
@patch(
    "src.services.forex.proposal_simulation.service.ExchangeCompanyApi.request_as_client",
    return_value=stub_caronte_response_success_22,
)
async def test_when_get_exchange_simulation_with_success_then_return_exchange_simulation_data(
    mock_request_caronte, mock_config
):
    result = await CustomerExchangeService._CustomerExchangeService__get_exchange_simulation_proposal_data_on_route_22(
        customer_token=stub_token_generated_in_route_21,
        customer_exchange_request_model=stub_customer_exchange_request_model,
    )

    assert isinstance(result, dict)


@pytest.mark.asyncio
@patch(
    "src.domain.models.forex.customer_exchange_request_data.model.config",
    side_effect=stub_config_path_exchange_simulation,
)
@patch(
    "src.services.forex.proposal_simulation.service.ExchangeCompanyApi.request_as_client",
    return_value=stub_caronte_response_bad_request,
)
async def test_when_get_exchange_simulation_result_is_bad_request_then_raises(
    mock_request_caronte, mock_config
):
    with pytest.raises(ExpiredToken):
        await CustomerExchangeService._CustomerExchangeService__get_exchange_simulation_proposal_data_on_route_22(
            customer_token=stub_token_generated_in_route_21,
            customer_exchange_request_model=stub_customer_exchange_request_model,
        )


@pytest.mark.asyncio
@patch(
    "src.domain.models.forex.customer_exchange_request_data.model.config",
    side_effect=stub_config_path_exchange_simulation,
)
@patch(
    "src.services.forex.proposal_simulation.service.ExchangeCompanyApi.request_as_client",
    return_value=stub_caronte_response_forbidden,
)
async def test_when_get_exchange_simulation_result_is_forbidden_then_raises(
    mock_request_caronte, mock_config
):
    with pytest.raises(DroppedToken):
        await CustomerExchangeService._CustomerExchangeService__get_exchange_simulation_proposal_data_on_route_22(
            customer_token=stub_token_generated_in_route_21,
            customer_exchange_request_model=stub_customer_exchange_request_model,
        )


@pytest.mark.asyncio
@patch(
    "src.domain.models.forex.customer_exchange_request_data.model.config",
    side_effect=stub_config_path_exchange_simulation,
)
@patch(
    "src.services.forex.proposal_simulation.service.ExchangeCompanyApi.request_as_client",
    return_value=stub_caronte_response_unauthorized,
)
async def test_when_get_exchange_simulation_result_is_unauthorized_then_raises(
    mock_request_caronte, mock_config
):
    with pytest.raises(InvalidToken):
        await CustomerExchangeService._CustomerExchangeService__get_exchange_simulation_proposal_data_on_route_22(
            customer_token=stub_token_generated_in_route_21,
            customer_exchange_request_model=stub_customer_exchange_request_model,
        )


@pytest.mark.asyncio
@patch(
    "src.domain.models.forex.customer_exchange_request_data.model.config",
    side_effect=stub_config_path_exchange_simulation,
)
@patch(
    "src.services.forex.proposal_simulation.service.ExchangeCompanyApi.request_as_client",
    return_value=stub_caronte_response_token_not_found,
)
async def test_when_get_exchange_simulation_result_is_token_not_found_then_raises(
    mock_request_caronte, mock_config
):
    with pytest.raises(CaronteCantFindToken):
        await CustomerExchangeService._CustomerExchangeService__get_exchange_simulation_proposal_data_on_route_22(
            customer_token=stub_token_generated_in_route_21,
            customer_exchange_request_model=stub_customer_exchange_request_model,
        )


@pytest.mark.asyncio
@patch(
    "src.domain.models.forex.customer_exchange_request_data.model.config",
    side_effect=stub_config_path_exchange_simulation,
)
@patch(
    "src.services.forex.proposal_simulation.service.ExchangeCompanyApi.request_as_client",
    return_value=stub_caronte_response_unexpected_error,
)
async def test_when_get_exchange_simulation_result_is_unexpected_error_then_raises(
    mock_request_caronte, mock_config
):
    with pytest.raises(UnexpectedErrorWhenTryingToGetExchangeSimulationProposal):
        await CustomerExchangeService._CustomerExchangeService__get_exchange_simulation_proposal_data_on_route_22(
            customer_token=stub_token_generated_in_route_21,
            customer_exchange_request_model=stub_customer_exchange_request_model,
        )


@pytest.mark.asyncio
async def test_when_have_token_data_then_return_customer_token_data():
    result = await CustomerExchangeService._CustomerExchangeService__validate_if_token_exists_in_content(
        content=stub_response_rote_21
    )

    assert isinstance(result, str)


@pytest.mark.asyncio
async def test_when_have_token_data_then_return_customer_token_data():
    with pytest.raises(CustomerQuotationTokenNotFound):
        await CustomerExchangeService._CustomerExchangeService__validate_if_token_exists_in_content(
            content={}
        )


@pytest.mark.asyncio
async def test_when_treatment_and_validation_with_success_then_return_exchange_simulation_data():
    result = await CustomerExchangeService._CustomerExchangeService__treatment_and_validation_exchange_simulation_data(
        exchange_simulation_proposal_data=stub_response_rote_22
    )

    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_when_treatment_and_validation_failed_then_raises():
    with pytest.raises(ErrorOnValidateExchangeSimulationProposalData):
        await CustomerExchangeService._CustomerExchangeService__treatment_and_validation_exchange_simulation_data(
            exchange_simulation_proposal_data=stub_response_missing_data_rote_22
        )


@pytest.mark.asyncio
@patch.object(
    CustomerExchangeService,
    "_CustomerExchangeService__get_exchange_simulation_proposal_data_on_route_22",
    return_value=stub_response_rote_22,
)
@patch.object(
    CustomerExchangeService,
    "_CustomerExchangeService__get_customer_token_on_route_21",
    return_value=stub_response_rote_21,
)
@patch.object(
    CustomerExchangeService,
    "_CustomerExchangeService__get_customer_exchange_account_data",
    return_value=stub_customer_exchange_data,
)
async def test_when_get_exchange_proposal_with_success_then_return_validated_exchange_simulation_proposal(
    mock_data, mock_route_21, mock_route_22
):
    result = await CustomerExchangeService.get_proposal_simulation(
        jwt_data={}, currency_exchange=stub_currency_exchange
    )

    assert isinstance(result, dict)
