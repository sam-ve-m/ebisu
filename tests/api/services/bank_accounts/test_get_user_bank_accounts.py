# Standard Libs
import pytest
from unittest.mock import patch, MagicMock

# INTERNAL LIBS
from tests.stubs.bank_account_stubs.stub_get_account import (jwt_data_dummy,
                                                             jwt_data_mist,
                                                             get_accounts_dummy)
from api.services.bank_account.service import UserBankAccountService
from api.repositories.bank_account.repository import UserBankAccountRepository
from api.repositories.base_repositories.mongo_db.base import MongoDbBaseRepository


@pytest.mark.asyncio
@patch.object(UserBankAccountRepository, 'get_registered_user_bank_accounts', return_value=get_accounts_dummy)
async def test_get_user_when_sending_the_right_params_then_return_all_the_accounts(mock_get_registered_user_bank_accounts):
    response = await UserBankAccountService.get_user_bank_accounts(jwt_data=jwt_data_dummy,
                                                                   bank_account_repository=UserBankAccountRepository)
    assert response == get_accounts_dummy
    assert isinstance(response, dict)
    assert response.get('bank_accounts')[0]["status"] == "active"


@pytest.mark.asyncio
@patch.object(UserBankAccountRepository, 'get_registered_user_bank_accounts', return_value=None)
async def test_get_user_when_sending_the_right_params_then_return_no_account_as_expected(mock_get_registered_user_bank_accounts):
    response = await UserBankAccountService.get_user_bank_accounts(jwt_data=jwt_data_dummy,
                                                                   bank_account_repository=UserBankAccountRepository)
    assert response == {"bank_accounts": []}
    assert isinstance(response, dict)
    assert response.get('bank_accounts') == []


@pytest.mark.asyncio
async def test_get_user_account_when_jwt_param_is_not_valid_then_raise_error_as_expected():
    with pytest.raises(AttributeError) as err:
        await UserBankAccountService.get_user_bank_accounts(jwt_data="",
                                                            bank_account_repository=UserBankAccountRepository)
        assert err == "'str' object has no attribute 'get'"


@pytest.mark.asyncio
async def test_get_user_account_when_the_bank_account_repository_is_not_valid_then_raise_error_as_expected():
    with pytest.raises(AttributeError) as err:
        await UserBankAccountService.get_user_bank_accounts(jwt_data=jwt_data_dummy,
                                                            bank_account_repository=None)
        assert err == "'NoneType' object has no attribute 'get_registered_user_bank_accounts'"
        assert err == AttributeError
