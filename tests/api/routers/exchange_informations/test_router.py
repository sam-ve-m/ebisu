# Standard Libs
import pytest
from unittest.mock import patch, AsyncMock, MagicMock

# INTERNAL LIBS
from api.routers.exchange_informations.router import ExchangeRouter
from api.services.jwt.service_jwt import JwtService
from tests.api.stubs.project_stubs.stub_data import payload_data_dummy
from api.services.get_balance.get_balance import GetBalance

# STUBS
balance_stub = {'payload': {'balance': 49030153.7}}


@pytest.mark.asyncio
@patch.object(JwtService, 'get_thebes_answer_from_request', return_value=payload_data_dummy)
@patch.object(GetBalance, 'get_service_response', return_value=balance_stub)
async def test_when_sending_the_right_params_to_get_balance_then_return_the_expected(
        mock_get_thebes_answer_from_request, mock_get_service_response
):
    response = await ExchangeRouter.get_balance(request=AsyncMock(), balance='BR')
    assert response == balance_stub
    assert 'payload' in response

#
# @pytest.mark.asyncio
# @patch.object(JwtService, 'get_thebes_answer_from_request', return_value=Exception)
# @patch.object(GetBalance, 'get_service_response')
# async def test_when_sending_the_wrong_params_to_get_balance_then_raise_error(
#         mock_get_thebes_answer_from_request, mock_get_service_response):
#     response = await ExchangeRouter.get_balance(request=MagicMock(), balance='BR')
#
#     assert response == ""

