# Standard Libs
import decouple
import pytest
from unittest.mock import patch, MagicMock

# INTERNAL LIBS
from decouple import RepositoryEnv
from persephone_client import Persephone
from tests.src.stubs.bank_account_stubs.stub_get_account import (
    jwt_with_bank_account_to_update,
)
from src.services.bank_account.service import UserBankAccountService
from src.repositories.bank_account.repository import UserBankAccountRepository
from src.domain.exception import BadRequestError, FailToSaveAuditingTrail
from tests.src.stubs.project_stubs.stub_data import payload_data_dummy


@pytest.mark.asyncio
@patch.object(
    UserBankAccountRepository, "user_bank_account_id_exists", return_value=True
)
@patch.object(
    UserBankAccountRepository, "update_registered_user_bank_accounts", return_value=True
)
@patch.object(UserBankAccountService, "bank_code_from_client_exists", return_value=True)
@patch.object(Persephone, "send_to_persephone", return_value=[True, True])
@patch.object(decouple, "RepositoryEnv", return_value="data")
async def test_update_user_when_sending_the_right_params_then_return_the_duly_updated_message(
        mock_repositoryenv,
        mock_send_to_persephone,
        mock_bank_code_from_client_exists,
        mock_update_registered_user_bank_accounts,
        mock_user_bank_account_id_exists
):
    response = await UserBankAccountService.update_user_bank_account(
        jwt_data=jwt_with_bank_account_to_update,
        bank_account_repository=UserBankAccountRepository,
    )
    updating_message = {"message": "Updated"}
    assert response == updating_message
    assert isinstance(response, dict)
    assert response.get("message") == "Updated"


@pytest.mark.asyncio
async def test_update_user_when_sending_an_invalid_jwt_data_then_return_the_expected_exception(
):
    with pytest.raises(KeyError):
        await UserBankAccountService.update_user_bank_account(
            jwt_data=payload_data_dummy,
            bank_account_repository=UserBankAccountRepository,
        )


@pytest.mark.asyncio
async def test_update_user_when_sending_an_invalid_bank_repository_call_then_return_the_expected_exception(
):
    with pytest.raises(AttributeError):
        await UserBankAccountService.update_user_bank_account(
            jwt_data=jwt_with_bank_account_to_update, bank_account_repository=""
        )


@pytest.mark.asyncio
@patch.object(
    UserBankAccountRepository, "user_bank_account_id_exists", return_value=False
)
@patch.object(
    UserBankAccountRepository,
    "update_registered_user_bank_accounts",
    return_value=False,
)
@patch.object(Persephone, "send_to_persephone", return_value=[True, False])
async def test_when_bank_account_and_register_account_are_false_then_raise_the_expected_bad_request(
        mock_get_registered_user_bank_accounts, mock_update_registered_user_bank_accounts, mock_send_to_persephone
):
    with pytest.raises(BadRequestError):
        await UserBankAccountService.update_user_bank_account(
            jwt_data=jwt_with_bank_account_to_update,
            bank_account_repository=UserBankAccountRepository,
        )


@pytest.mark.asyncio
@patch.object(UserBankAccountRepository, "user_bank_account_id_exists", return_value=True)
@patch.object(UserBankAccountRepository, "update_registered_user_bank_accounts", return_value=False)
@patch.object(Persephone, "send_to_persephone", return_value=[False, False])
@patch.object(decouple, "RepositoryEnv", return_value=MagicMock())
async def test_when_register_account_is_false_then_raise_the_expected_fail_to_save_auditing_trail(
    mock_repository_env,
    mock_send_to_persephone,
    mock_update_registered_user_bank_accounts,
    mock_user_bank_account_id_exists
):
    with pytest.raises(FailToSaveAuditingTrail):
        await UserBankAccountService.update_user_bank_account(
            jwt_data=jwt_with_bank_account_to_update,
            bank_account_repository=UserBankAccountRepository,
        )


@pytest.mark.asyncio
async def test_when_sending_wrong_params_of_repository_then_raise_key_error_as_expected():
    with pytest.raises(AttributeError):
        await UserBankAccountService.update_user_bank_account(
            bank_account_repository=None, jwt_data=jwt_with_bank_account_to_update
        )


@pytest.mark.asyncio
async def test_when_jwt_data_payload_is_invalid_then_raise_type_error_as_expected():
    with pytest.raises(TypeError):
        await UserBankAccountService.update_user_bank_account(
            jwt_data=None, bank_account_repository=UserBankAccountRepository
        )
