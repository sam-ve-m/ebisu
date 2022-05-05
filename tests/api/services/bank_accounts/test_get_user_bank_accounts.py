# Standard Libs
import pytest
from unittest.mock import patch

# INTERNAL LIBS
from tests.stubs.bank_account_stubs.stub_get_account import jwt_data_dummy, get_accounts_dummy
from api.services.bank_account.service import UserBankAccountService
from api.repositories.bank_account.repository import UserBankAccountRepository


@pytest.mark.asyncio
@patch.object(UserBankAccountRepository, 'get_registered_user_bank_accounts', return_value=get_accounts_dummy)
async def test_get_user_when_sending_the_right_params_then_return_all_the_accounts(
        mock_get_registered_user_bank_accounts):

    response = await UserBankAccountService.get_user_bank_accounts(jwt_data=jwt_data_dummy,
                                                                   bank_account_repository=UserBankAccountRepository)
    assert response == get_accounts_dummy
    assert isinstance(response, dict)
    assert response.get('bank_accounts')[0]["status"] == "active"


@pytest.mark.asyncio
@patch.object(UserBankAccountRepository, 'get_registered_user_bank_accounts', return_value=None)
async def test_get_user_when_sending_the_right_params_then_return_no_account_as_expected(
        mock_get_registered_user_bank_accounts):
    none_data_stub = {"bank_accounts": []}

    response = await UserBankAccountService.get_user_bank_accounts(jwt_data=jwt_data_dummy,
                                                                   bank_account_repository=UserBankAccountRepository)
    assert response == none_data_stub
    assert isinstance(response, dict)
    assert response.get('bank_accounts') == []


@pytest.mark.asyncio
async def test_get_user_account_when_jwt_param_is_not_valid_then_raise_error_as_expected():
    with pytest.raises(TypeError):
        await UserBankAccountService.get_user_bank_accounts(jwt_data={},
                                                            bank_account_repository=UserBankAccountRepository)


@pytest.mark.asyncio
async def test_get_user_account_when_the_bank_account_repository_is_not_valid_then_raise_error_as_expected():
    with pytest.raises(AttributeError):
        await UserBankAccountService.get_user_bank_accounts(jwt_data=jwt_data_dummy,
                                                            bank_account_repository=None)
