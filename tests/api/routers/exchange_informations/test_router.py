# Standard Libs
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi import Request

# INTERNAL LIBS
from api.domain.validators.exchange_info.get_balance_validator import GetBalanceModel
from api.routers.exchange_informations.router import ExchangeRouter
from api.services.jwt.service_jwt import JwtService
from tests.api.stubs.project_stubs.stub_data import payload_data_dummy
from api.services.get_balance.get_balance import GetBalance
from api.exceptions.exceptions import UnauthorizedError

# STUBS
balance_stub = {'payload': {'balance': 49030153.7}}
scope_stub = {'type': 'http', 'headers': {'x-thebes-answer': None}}

scope_stub_2 = {'type': 'http', 'headers': {'x-thebes-answer': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJleHAiOiAxNjc4MjA5Nzg4LCAiY3JlYXRlZF9hdCI6IDE2NDY2NzM3ODguNDQyMTM5LCAic2NvcGUiOiB7InZpZXdfdHlwZSI6ICJkZWZhdWx0IiwgInVzZXJfbGV2ZWwiOiAiY2xpZW50IiwgImZlYXR1cmVzIjogWyJkZWZhdWx0IiwgInJlYWx0aW1lIl19LCAidXNlciI6IHsidW5pcXVlX2lkIjogIjQwZGI3ZmVlLTZkNjAtNGQ3My04MjRmLTFiZjg3ZWRjNDQ5MSIsICJuaWNrX25hbWUiOiAiUkFTVDMiLCAicG9ydGZvbGlvcyI6IHsiYnIiOiB7ImJvdmVzcGFfYWNjb3VudCI6ICIwMDAwMDAwMTQtNiIsICJibWZfYWNjb3VudCI6ICIxNCJ9LCAidXMiOiB7Il8iOiBudWxsfX0sICJjbGllbnRfaGFzX2JyX3RyYWRlX2FsbG93ZWQiOiBmYWxzZSwgImNsaWVudF9oYXNfdXNfdHJhZGVfYWxsb3dlZCI6IGZhbHNlLCAiY2xpZW50X3Byb2ZpbGUiOiAiaW52ZXN0b3IifX0.ccXheG6ORUWlsOmp0iZnyx39aEgW9zIEtL9Tf3aZ4bXXz_pIwI9f8LW15MHYjyvrkCjjb6dEuxQSqwxbYQvPdwq2PTJ0kLROYnDx8v0z9CX6WYHiLDapWHRoosgGUU20x1hqD_k_GSvpw_7DEyKkXavAJtK7XvwnZToFyWb1F1UhTVFsr_Oybh2PDsi6NvVgd3fhs17GVI81DmWFcBfz4J01S_446P-xmgfHjlOTatCKR1_0I2oDKeLi2fH160xXfApqfT5nOq9vsui-WaoI87_noUc3CQXk2BvqfFu83TRk2sIj4xKZp633DtCyM8D6iJngNPclH-K6o23EwSSa1g'}}

x_thebes_tuple = [(b'x-thebes-answer', b'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJleHAiOiAxNjc4MjA5Nzg4LCAiY3JlYXRlZF9hdCI6IDE2NDY2NzM3ODguNDQyMTM5LCAic2NvcGUiOiB7InZpZXdfdHlwZSI6ICJkZWZhdWx0IiwgInVzZXJfbGV2ZWwiOiAiY2xpZW50IiwgImZlYXR1cmVzIjogWyJkZWZhdWx0IiwgInJlYWx0aW1lIl19LCAidXNlciI6IHsidW5pcXVlX2lkIjogIjQwZGI3ZmVlLTZkNjAtNGQ3My04MjRmLTFiZjg3ZWRjNDQ5MSIsICJuaWNrX25hbWUiOiAiUkFTVDMiLCAicG9ydGZvbGlvcyI6IHsiYnIiOiB7ImJvdmVzcGFfYWNjb3VudCI6ICIwMDAwMDAwMTQtNiIsICJibWZfYWNjb3VudCI6ICIxNCJ9LCAidXMiOiB7Il8iOiBudWxsfX0sICJjbGllbnRfaGFzX2JyX3RyYWRlX2FsbG93ZWQiOiBmYWxzZSwgImNsaWVudF9oYXNfdXNfdHJhZGVfYWxsb3dlZCI6IGZhbHNlLCAiY2xpZW50X3Byb2ZpbGUiOiAiaW52ZXN0b3IifX0.ccXheG6ORUWlsOmp0iZnyx39aEgW9zIEtL9Tf3aZ4bXXz_pIwI9f8LW15MHYjyvrkCjjb6dEuxQSqwxbYQvPdwq2PTJ0kLROYnDx8v0z9CX6WYHiLDapWHRoosgGUU20x1hqD_k_GSvpw_7DEyKkXavAJtK7XvwnZToFyWb1F1UhTVFsr_Oybh2PDsi6NvVgd3fhs17GVI81DmWFcBfz4J01S_446P-xmgfHjlOTatCKR1_0I2oDKeLi2fH160xXfApqfT5nOq9vsui-WaoI87_noUc3CQXk2BvqfFu83TRk2sIj4xKZp633DtCyM8D6iJngNPclH-K6o23EwSSa1g')]


@pytest.mark.asyncio
@patch.object(GetBalance, 'get_service_response', return_value=balance_stub)
async def test_when_sending_the_right_params_to_get_balance_then_return_the_expected(
        mock_get_service_response
):
    MagicMock(return_value='abc')

    response = await ExchangeRouter.get_balance(
        request=MagicMock(scope=scope_stub_2, headers=MagicMock(raw=x_thebes_tuple)),
        balance=GetBalanceModel(**{"region": 'BR'}))

    assert response == balance_stub
    assert 'payload' in response


@pytest.mark.asyncio
@patch.object(GetBalance, 'get_service_response')
async def test_when_sending_the_wrong_params_to_get_balance_then_raise_error(
        mock_get_service_response):
    with pytest.raises(UnauthorizedError):
        await ExchangeRouter.get_balance(request=MagicMock(scope=scope_stub), balance=GetBalanceModel(**{"region": 'BR'}))
        mock_get_service_response.assert_not_called()
