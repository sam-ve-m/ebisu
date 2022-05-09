# Standard Libs
import pytest
from unittest.mock import patch

# INTERNAL LIBS
from tests.api.stubs.bank_account_stubs.stub_get_account import jwt_with_bank_account_to_delete
from api.services.bank_account.service import UserBankAccountService
from api.repositories.bank_account.repository import UserBankAccountRepository
from api.exceptions.exceptions import BadRequestError, InternalServerError
from tests.api.stubs.project_stubs.stub_data import payload_data_dummy


@pytest.mark.asyncio
@patch.object(UserBankAccountRepository, 'user_bank_account_id_exists', return_value=True)
@patch.object(UserBankAccountRepository, 'delete_registered_user_bank_accounts', return_value=True)
async def test_delete_user_when_sending_the_right_params_then_return_the_duly_updated_message(
        mock_get_registered_user_bank_accounts, mock_delete_registered_user_bank_accounts):

    response = await UserBankAccountService.delete_user_bank_account(jwt_data=jwt_with_bank_account_to_delete,
                                                                   bank_account_repository=UserBankAccountRepository)
    dully_deleted_response = {"message": "Deleted"}

    assert response == dully_deleted_response
    assert isinstance(response, dict)
    assert response.get('message') == "Deleted"


@pytest.mark.asyncio
async def test_delete_user_when_sending_an_invalid_jwt_data_then_return_the_expected_exception():
    with pytest.raises(KeyError):
        await UserBankAccountService.delete_user_bank_account(jwt_data=payload_data_dummy,
                                                              bank_account_repository=UserBankAccountRepository)


@pytest.mark.asyncio
async def test_delete_user_when_sending_an_invalid_bank_repository_call_then_return_the_expected_attribute_exception():
    with pytest.raises(AttributeError):
        await UserBankAccountService.delete_user_bank_account(jwt_data=jwt_with_bank_account_to_delete,
                                                                     bank_account_repository="")


@pytest.mark.asyncio
@patch.object(UserBankAccountRepository, 'user_bank_account_id_exists', return_value=False)
@patch.object(UserBankAccountRepository, 'delete_registered_user_bank_accounts', return_value=False)
async def test_when_bank_account_and_register_account_are_false_then_raise_the_expected_bad_request(
        mock_get_registered_user_bank_accounts, mock_update_registered_user_bank_accounts):

    with pytest.raises(BadRequestError):
        await UserBankAccountService.delete_user_bank_account(jwt_data=jwt_with_bank_account_to_delete,
                                                              bank_account_repository=UserBankAccountRepository)


@pytest.mark.asyncio
@patch.object(UserBankAccountRepository, 'user_bank_account_id_exists', return_value=True)
@patch.object(UserBankAccountRepository, 'delete_registered_user_bank_accounts', return_value=False)
async def test_when_register_account_is_false_then_raise_the_expected_internal_server_error(
        mock_get_registered_user_bank_accounts, mock_update_registered_user_bank_accounts):

    with pytest.raises(InternalServerError):
        await UserBankAccountService.delete_user_bank_account(jwt_data=jwt_with_bank_account_to_delete,
                                                              bank_account_repository=UserBankAccountRepository)


@pytest.mark.asyncio
async def test_when_sending_wrong_params_then_return_an_empty_object():
    with pytest.raises(AttributeError):
        response = await UserBankAccountService.delete_user_bank_account(  bank_account_repository="",
                                                                            jwt_data=jwt_with_bank_account_to_delete)
        assert response == "'NoneType' object has no attribute 'lower'"


@pytest.mark.asyncio
async def test_when_jwt_data_payload_is_invalid_then_check_if_portfolios_is_in_the_payload_response():
    with pytest.raises(TypeError) as err:
        response = await UserBankAccountService.delete_user_bank_account(jwt_data="",
                                                                        bank_account_repository=UserBankAccountRepository)
        assert response == "string indices must be integers"
