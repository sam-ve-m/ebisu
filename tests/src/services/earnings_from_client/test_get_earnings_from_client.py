# STANDARD LIBS
import pytest
from unittest.mock import patch

# external imports
from pydantic import ValidationError

from src.domain.earning.br.response.model import BrEarningsModelToResponse
from src.repositories.earnings.repository import EarningsBrRecord
from src.services.earnings_from_client.earnings_stub import get_br_payable_earnings_stub, \
    get_br_record_date_earnings_stub, get_br_paid_earnings_stub, get_earnings_response_stub
from src.services.earnings_from_client.get_earnings_from_client import (
    EarningsFromClient,
)
from src.domain.validators.exchange_info.get_earnings_client import EarningsClientModel
from tests.src.stubs.project_stubs.stub_data import payload_data_dummy


@pytest.mark.asyncio
@patch.object(EarningsBrRecord, "get_br_payable_earnings", return_value=get_br_payable_earnings_stub)
@patch.object(EarningsBrRecord, "get_br_paid_earnings", return_value=get_br_paid_earnings_stub)
@patch.object(EarningsBrRecord, "get_br_record_date_earnings", return_value=get_br_record_date_earnings_stub)
@patch.object(BrEarningsModelToResponse, "earnings_response", return_value=get_earnings_response_stub)
async def test_get_earnings_client_br_account_when_sending_right_params_then_return_the_expected(
        mock_get_br_payable_earnings,
        mock_get_br_paid_earnings,
        mock_get_br_record_date_earnings,
        mock_earnings_response
):
    response = await EarningsFromClient.get_earnings_client_br_account(
        jwt_data=payload_data_dummy, earnings_client=EarningsClientModel(
            **{"region": "BR", "limit": 2, "offset": 0}
        )
    )
    assert response == get_earnings_response_stub
    assert isinstance(response, list)


async def test_get_earnings_client_br_account_when_sending_wrong_params_then_return_error():
    with pytest.raises(AttributeError):
        await EarningsFromClient.get_earnings_client_br_account(
            jwt_data=payload_data_dummy, earnings_client=EarningsClientModel(
                **{"region": None, "limit": None, "offset": 0}
            )
        )


def test_earnings_from_client_response_when_the_params_are_not_valid_then_raise_error_as_expected():
    with pytest.raises(ValidationError):
        EarningsFromClient.get_service_response(
            earnings_client=EarningsClientModel(
                **{"region": None, "limit": None, "offset": None}
            ),
            jwt_data=payload_data_dummy,
        )


@pytest.mark.asyncio
async def test_earnings_from_client_response_when_the_jwt_is_not_valid_then_raise_error_as_expected():
    with pytest.raises(AttributeError):
        await EarningsFromClient.get_service_response(
            earnings_client=EarningsClientModel(
                **{"region": "BR", "limit": 2, "offset": 0}
            ),
            jwt_data=None,
        )
