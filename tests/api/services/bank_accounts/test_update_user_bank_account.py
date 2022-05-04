# Standard Libs
import pytest
from unittest.mock import patch, MagicMock

# INTERNAL LIBS
from tests.stubs.bank_account_stubs.stub_get_account import (jwt_data_dummy,
                                                             jwt_data_mist,
                                                             jwt_with_bank_account_to_update,
                                                             get_accounts_dummy)
from api.services.bank_account.service import UserBankAccountService
from api.repositories.bank_account.repository import UserBankAccountRepository
from api.repositories.base_repositories.mongo_db.base import MongoDbBaseRepository


@pytest.mark.asyncio
async def test_update_user_account_when_jwt_param_is_not_valid_then_raise_error_as_expected():
    with pytest.raises(TypeError) as err:
        await UserBankAccountService.update_user_bank_account(jwt_data="",
                                                            bank_account_repository=UserBankAccountRepository)
        assert err == "string indices must be integers"
        assert err == TypeError


@pytest.mark.asyncio
async def test_update_user_account_when_the_bank_account_repository_is_not_valid_then_raise_error_as_expected():
    with pytest.raises(AttributeError) as err:
        await UserBankAccountService.get_user_bank_accounts(jwt_data=jwt_data_dummy,
                                                            bank_account_repository=None)
        assert err == AttributeError


@pytest.mark.asyncio
@patch.object(UserBankAccountRepository, 'user_bank_account_id_exists', return_value=True)
@patch.object(UserBankAccountRepository, 'update_registered_user_bank_accounts', return_value=True)
async def test_update_user_when_sending_the_right_params_then_return_the_duly_updated_message(
        mock_get_registered_user_bank_accounts, mock_update_registered_user_bank_accounts):
    response = await UserBankAccountService.get_user_bank_accounts(jwt_data=jwt_with_bank_account_to_update,
                                                                   bank_account_repository=UserBankAccountRepository)
    updating_message = {"message": "Updated"}

    assert response == updating_message
    assert isinstance(response, dict)
    assert response.get('message') == "Updated"


