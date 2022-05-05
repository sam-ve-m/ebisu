# Standard Libs
import pytest
from unittest.mock import patch

# INTERNAL LIBS
from tests.stubs.bank_account_stubs.stub_get_account import jwt_with_bank_account_to_update
from api.services.bank_account.service import UserBankAccountService
from api.repositories.bank_account.repository import UserBankAccountRepository
from api.exceptions.exceptions import BadRequestError, InternalServerError
from tests.stubs.project_stubs.stub_data import payload_data_dummy


@pytest.mark.asyncio
@patch.object(UserBankAccountRepository, 'user_bank_account_id_exists', return_value=True)
@patch.object(UserBankAccountRepository, 'update_registered_user_bank_accounts', return_value=True)
async def test_update_user_when_sending_the_right_params_then_return_the_duly_updated_message(
        mock_get_registered_user_bank_accounts, mock_update_registered_user_bank_accounts):

    response = await UserBankAccountService.update_user_bank_account(jwt_data=jwt_with_bank_account_to_update,
                                                                   bank_account_repository=UserBankAccountRepository)
    
    updating_message = {"message": "Updated"}

    assert response == updating_message
    assert isinstance(response, dict)
    assert response.get('message') == "Updated"


@pytest.mark.asyncio
@patch.object(UserBankAccountRepository, 'user_bank_account_id_exists', return_value=True)
@patch.object(UserBankAccountRepository, 'update_registered_user_bank_accounts', return_value=True)
async def test_update_user_when_sending_an_invalid_jwt_data_then_return_the_expected_exception(
        mock_get_registered_user_bank_accounts, mock_update_registered_user_bank_accounts):

    with pytest.raises(KeyError):
        await UserBankAccountService.update_user_bank_account(jwt_data=payload_data_dummy,
                                                              bank_account_repository=UserBankAccountRepository)


@pytest.mark.asyncio
@patch.object(UserBankAccountRepository, 'user_bank_account_id_exists', return_value=True)
@patch.object(UserBankAccountRepository, 'update_registered_user_bank_accounts', return_value=True)
async def test_update_user_when_sending_an_invalid_bank_repository_call_then_return_the_expected_exception(
        mock_get_registered_user_bank_accounts, mock_update_registered_user_bank_accounts):

    with pytest.raises(AttributeError):
        await UserBankAccountService.update_user_bank_account(jwt_data=jwt_with_bank_account_to_update,
                                                                     bank_account_repository="")


@pytest.mark.asyncio
@patch.object(UserBankAccountRepository, 'user_bank_account_id_exists', return_value=False)
@patch.object(UserBankAccountRepository, 'update_registered_user_bank_accounts', return_value=False)
async def test_when_bank_account_and_register_account_are_false_then_raise_the_expected_bad_request(
        mock_get_registered_user_bank_accounts, mock_update_registered_user_bank_accounts):

    with pytest.raises(BadRequestError):
        await UserBankAccountService.update_user_bank_account(jwt_data=jwt_with_bank_account_to_update,
                                                              bank_account_repository=UserBankAccountRepository)


@pytest.mark.asyncio
@patch.object(UserBankAccountRepository, 'user_bank_account_id_exists', return_value=True)
@patch.object(UserBankAccountRepository, 'update_registered_user_bank_accounts', return_value=False)
async def test_when_register_account_is_false_then_raise_the_expected_internal_server_error(
        mock_get_registered_user_bank_accounts, mock_update_registered_user_bank_accounts):

    with pytest.raises(InternalServerError):
        await UserBankAccountService.update_user_bank_account(jwt_data=jwt_with_bank_account_to_update,
                                                              bank_account_repository=UserBankAccountRepository)
