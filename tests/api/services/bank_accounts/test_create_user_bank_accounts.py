# Standard Libs
import pytest
from unittest.mock import patch

# INTERNAL LIBS
from tests.stubs.bank_account_stubs.stub_get_account import jwt_with_bank_account_to_create
from api.services.bank_account.service import UserBankAccountService
from api.repositories.bank_account.repository import UserBankAccountRepository
from api.exceptions.exceptions import BadRequestError, InternalServerError
from tests.stubs.project_stubs.stub_data import payload_data_dummy


@pytest.mark.asyncio



@pytest.mark.asyncio
@patch.object(UserBankAccountRepository, 'is_user_bank_account_from_client', return_value=True)
@patch.object(UserBankAccountRepository, 'existing_user_bank_account_and_is_activated', return_value=False)
@patch.object(UserBankAccountRepository, 'save_registered_user_bank_accounts', return_value=True)
async def test_create_user_when_sending_the_right_params_then_return_the_duly_deleted_message(
        mock_user_bank_account_from_client,
        mock_existing_user_bank_account_and_is_activated,
        mock_save_registered_user_bank_accounts):
    response = await UserBankAccountService.create_user_bank_accounts(bank_account_repository=UserBankAccountRepository,
                                                                      jwt_data=jwt_with_bank_account_to_create)
    assert response == {'message': 'Created'}


@pytest.mark.asyncio
@patch.object(UserBankAccountRepository, 'is_user_bank_account_from_client', return_value=True)
@patch.object(UserBankAccountRepository, 'existing_user_bank_account_and_is_activated', return_value=True)
async def test_create_user_when_sending_the_right_params_but_account_is_from_user_and_account_is_already_activated(
        mock_user_bank_account_from_client, mock_existing_user_bank_account_and_is_activated):

    with pytest.raises(BadRequestError):
        await UserBankAccountService.create_user_bank_accounts(jwt_data=jwt_with_bank_account_to_create,
                                                                bank_account_repository=UserBankAccountRepository)


@pytest.mark.asyncio
@patch.object(UserBankAccountRepository, 'is_user_bank_account_from_client', return_value=False)
@patch.object(UserBankAccountRepository, 'existing_user_bank_account_and_is_activated', return_value=False)
@patch.object(UserBankAccountRepository, 'save_registered_user_bank_accounts', return_value=True)
async def test_create_user_when_sending_the_right_params_and_bank_account_is_not_activated_and_account_is_not_from_client(
        mock_user_bank_account_from_client,
        mock_existing_user_bank_account_and_is_activated,
        save_registered_user_bank_accounts):

    with pytest.raises(BadRequestError):
        await UserBankAccountService.create_user_bank_accounts(jwt_data=jwt_with_bank_account_to_create,
                                                                bank_account_repository=UserBankAccountRepository)


@pytest.mark.asyncio
@patch.object(UserBankAccountRepository, 'is_user_bank_account_from_client', return_value=True)
@patch.object(UserBankAccountRepository, 'existing_user_bank_account_and_is_activated', return_value=False)
@patch.object(UserBankAccountRepository, 'save_registered_user_bank_accounts', return_value=False)
async def test_create_user_when_sending_the_right_params_but_account_is_activated_and_saved(
        mock_user_bank_account_from_client,
        mock_existing_user_bank_account_and_is_activated,
        mock_save_registered_user_bank_accounts):

    with pytest.raises(InternalServerError):
        await UserBankAccountService.create_user_bank_accounts(jwt_data=jwt_with_bank_account_to_create,
                                                                bank_account_repository=UserBankAccountRepository)

@pytest.mark.asyncio
async def test_when_sending_wrong_params_then_return_an_empty_object():
    with pytest.raises(AttributeError):
        response = await UserBankAccountService.create_user_bank_accounts(  bank_account_repository="",
                                                                            jwt_data=jwt_with_bank_account_to_create)
        assert response == "'NoneType' object has no attribute 'lower'"

@pytest.mark.asyncio
async def test_when_jwt_data_payload_is_invalid_then_check_if_portfolios_is_in_the_payload_response():
    with pytest.raises(TypeError) as err:
        response = await UserBankAccountService.create_user_bank_accounts(  jwt_data="",
                                                                            bank_account_repository=UserBankAccountRepository)
        assert response == "string indices must be integers"
