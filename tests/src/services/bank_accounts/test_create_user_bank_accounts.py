# Standard Libs
import decouple
import pytest
from unittest.mock import patch, MagicMock
import logging.config
from persephone_client import Persephone
from copy import deepcopy

# PROJECT IMPORTS
from decouple import Config, RepositoryEnv

from src.domain.exceptions.service.auditing_trail.model import FailToSaveAuditingTrail
from src.domain.exceptions.service.unexpected.internal_server_error.model import (
    InternalServerError,
)

# INTERNAL LIBS
from src.services.bank_account.service import UserBankAccountService
from src.repositories.bank_account.repository import UserBankAccountRepository

# STUB FILES
from tests.src.stubs.bank_account_stubs.stub_get_account import (
    jwt_with_bank_account_to_create,
)


@pytest.mark.asyncio
@patch.object(
    UserBankAccountRepository,
    "existing_user_bank_account_and_is_activated",
    return_value=False,
)
@patch.object(
    UserBankAccountRepository, "save_registered_user_bank_accounts", return_value=True
)
@patch.object(UserBankAccountService, "bank_code_from_client_exists", return_value=True)
@patch.object(Persephone, "send_to_persephone", return_value=[True, True])
@patch.object(Config, "get", return_value="lala")
async def test_create_user_when_sending_the_right_params_then_return_the_duly_deleted_message(
    mock_send_to_persephone,
    mock_bank_code_from_client_exists,
    mock_save_registered_user_bank_accounts,
    mock_existing_user_bank_account_and_is_activated,
    mock_get,
):

    jwt_data = deepcopy(jwt_with_bank_account_to_create)

    response = await UserBankAccountService.create_user_bank_accounts(
        bank_account_repository=UserBankAccountRepository,
        jwt_data=jwt_data,
    )
    assert response == {"message": "Created"}
    assert isinstance(response, dict)


@pytest.mark.asyncio
@patch.object(
    UserBankAccountRepository,
    "existing_user_bank_account_and_is_activated",
    return_value=False,
)
@patch.object(
    UserBankAccountRepository, "save_registered_user_bank_accounts", return_value=True
)
@patch.object(UserBankAccountService, "bank_code_from_client_exists", return_value=True)
@patch.object(Persephone, "send_to_persephone", return_value=[False, True])
@patch.object(Config, "get", return_value="lala")
async def test_create_user_when_sending_the_right_params_but_account_is_from_user_and_account_is_already_activated(
    mock_existing_user_bank_account_and_is_activated,
    mock_save_registered_user_bank_accounts,
    mock_bank_code_from_client_exists,
    mock_send_to_persephone,
    repository_env,
):
    jwt_data = deepcopy(jwt_with_bank_account_to_create)
    with pytest.raises(FailToSaveAuditingTrail):
        await UserBankAccountService.create_user_bank_accounts(
            jwt_data=jwt_data,
            bank_account_repository=UserBankAccountRepository,
        )


@pytest.mark.asyncio
@patch.object(
    UserBankAccountRepository,
    "existing_user_bank_account_and_is_activated",
    return_value=False,
)
@patch.object(
    UserBankAccountRepository, "save_registered_user_bank_accounts", return_value=True
)
@patch.object(UserBankAccountService, "bank_code_from_client_exists", return_value=True)
@patch.object(Persephone, "send_to_persephone", return_value=[False, False])
@patch.object(Config, "get", return_value="lala")
async def test_when_sending_the_right_params_and_bank_account_is_not_activated_then_raise_fail_to_save(
    mock_send_to_persephone,
    mock_bank_code_from_client_exists,
    mock_save_registered_user_bank_accounts,
    mock_existing_user_bank_account_and_is_activated,
    mock_get,
):
    jwt_data = deepcopy(jwt_with_bank_account_to_create)
    with pytest.raises(FailToSaveAuditingTrail):
        await UserBankAccountService.create_user_bank_accounts(
            jwt_data=jwt_data,
            bank_account_repository=UserBankAccountRepository,
        )


@pytest.mark.asyncio
@patch.object(
    UserBankAccountRepository,
    "existing_user_bank_account_and_is_activated",
    return_value=False,
)
@patch.object(
    UserBankAccountRepository, "save_registered_user_bank_accounts", return_value=False
)
@patch.object(UserBankAccountService, "bank_code_from_client_exists", return_value=True)
@patch.object(Persephone, "send_to_persephone", return_value=[True, True])
@patch.object(Config, "get", return_value="lala")
async def test_create_user_when_sending_the_right_params_but_account_is_activated_and_saved(
    mock_send_to_persephone,
    mock_bank_code_from_client_exists,
    mock_save_registered_user_bank_accounts,
    mock_existing_user_bank_account_and_is_activated,
    mock_get,
):
    jwt_data = deepcopy(jwt_with_bank_account_to_create)

    with pytest.raises(InternalServerError):
        await UserBankAccountService.create_user_bank_accounts(
            jwt_data=jwt_data,
            bank_account_repository=UserBankAccountRepository,
        )


@pytest.mark.asyncio
async def test_when_sending_wrong_params_of_bank_account_repository_then_raise_attribute_error():
    jwt_data = deepcopy(jwt_with_bank_account_to_create)
    with pytest.raises(AttributeError):
        await UserBankAccountService.create_user_bank_accounts(
            bank_account_repository=None, jwt_data=jwt_data
        )


@pytest.mark.asyncio
async def test_when_jwt_data_payload_is_invalid_then_raise_type_error_as_expected():
    with pytest.raises(TypeError):
        await UserBankAccountService.create_user_bank_accounts(
            jwt_data=None, bank_account_repository=UserBankAccountRepository
        )
