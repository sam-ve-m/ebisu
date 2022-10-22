# STANDARD IMPORTS
from typing import List

import pytest
from unittest.mock import patch
from pydantic import ValidationError

# PROJECT IMPORTS
from src.domain.earning.br.response.model import BrEarningsModelToResponse
from src.repositories.earnings.repository import EarningsBrRecord
from src.domain.request.exchange_info.get_earnings_client import EarningsClientModel
from src.services.earnings_from_client.get_earnings_from_client import (
    EarningsFromClient,
)

# STUBS IMPORTS
from tests.src.services.earnings_from_client.stub_earnings import (
    get_br_payable_earnings_stub,
    get_br_record_date_earnings_stub,
    get_br_paid_earnings_stub,
    get_earnings_response_stub,
    stub_get_service_response,
)
from tests.src.stubs.project_stubs.stub_data import payload_data_dummy


# MUDOU HOTFIX 1.0.12


@pytest.mark.asyncio
@patch.object(
    EarningsBrRecord,
    "get_total_paid_earnings",
    return_value=10.0,
)
@patch.object(
    EarningsBrRecord,
    "get_br_payable_earnings",
    return_value=get_br_payable_earnings_stub,
)
@patch.object(
    EarningsBrRecord, "get_br_paid_earnings", return_value=get_br_paid_earnings_stub
)
@patch.object(
    EarningsBrRecord,
    "get_br_record_date_earnings",
    return_value=get_br_record_date_earnings_stub,
)
@patch.object(
    BrEarningsModelToResponse,
    "earnings_response",
    return_value=get_earnings_response_stub,
)
async def test_get_earnings_client_br_account_when_sending_right_params_then_return_the_expected(
    mock_total_paid_earnings,
    mock_get_br_payable_earnings,
    mock_get_br_paid_earnings,
    mock_get_br_record_date_earnings,
    mock_earnings_response,
):
    response = await EarningsFromClient.get_earnings_client_br_account(
        jwt_data=payload_data_dummy,
        earnings_client=EarningsClientModel(**{"region": "BR", "limit": 2}),
    )
    assert response == get_earnings_response_stub
    assert isinstance(response, list)


@pytest.mark.asyncio
@patch.object(
    EarningsFromClient,
    "get_earnings_client_br_account",
    return_value=stub_get_service_response,
)
async def test_get_service_response_when_sending_right_params_then_return_expected(
    mock_get_earnings_client_br_account,
):
    response = await EarningsFromClient.get_service_response(
        earnings_client=EarningsClientModel(**{"region": "BR", "limit": 1}),
        jwt_data=payload_data_dummy,
    )
    assert response == stub_get_service_response
    assert isinstance(response, dict)


@pytest.mark.asyncio
async def test_get_earnings_client_br_account_when_sending_wrong_params_then_return_validation_error():
    with pytest.raises(ValidationError):
        await EarningsFromClient.get_earnings_client_br_account(
            jwt_data=payload_data_dummy,
            earnings_client=EarningsClientModel(**{"region": None, "limit": None}),
        )


def test_earnings_from_client_response_when_the_params_are_not_valid_then_raise_error_as_expected():
    with pytest.raises(ValidationError):
        EarningsFromClient.get_service_response(
            earnings_client=EarningsClientModel(**{"region": None, "limit": None}),
            jwt_data=payload_data_dummy,
        )


@pytest.mark.asyncio
async def test_earnings_from_client_response_when_the_jwt_is_not_valid_then_raise_error_as_expected():
    with pytest.raises(AttributeError):
        await EarningsFromClient.get_service_response(
            earnings_client=EarningsClientModel(**{"region": "BR", "limit": 2}),
            jwt_data=None,
        )
