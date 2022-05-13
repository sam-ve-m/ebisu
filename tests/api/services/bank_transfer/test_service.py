# Standard Libs
import pytest
from unittest.mock import patch, MagicMock

# External Libs
from api.services.bank_transfer.service import BankTransferService
from tests.api.stubs.router_bank_accounts_stubs.stubs import x_thebes_bank_tuple

# stub
jwt_decompiled_stub = {'exp': 1678209788, 'created_at': 1646673788.442139, 'scope':
    {'view_type': 'default', 'user_level': 'client'},
                       'user':
                           {'unique_id': '40db7fee-6d60-4d73-824f-1bf87edc4491', 'nick_name': 'RAST3', 'portfolios':
                               {'br': {'bovespa_account': '000000014-6', 'bmf_account': '14'},
                                'us': {'_': None}}}}
jwt_data = {'CLIENT_JWT_NAME': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9'}
response_stub = {"agency": "0001", "bank": "001", "account": "000000014-6"}


@pytest.mark.asyncio
@patch('api.services.jwt.service.jwt_validator_and_decompile', return_value=jwt_decompiled_stub)
@patch('api.services.jwt.service.verify_jwt_token_by_string', return_value=jwt_decompiled_stub)
async def test_when_sending_the_right_jwt_then_return_the_bank_account_datas_from_jwt(
        mock_jwt_validator_and_decompile, mock_verify_jwt_token_by_string):
    response = await BankTransferService.get_bank_transfer_account(
        request=MagicMock(headers=MagicMock(raw=x_thebes_bank_tuple)))
    assert response == response_stub

