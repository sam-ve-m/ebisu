# Standard Libs
import os
import mock
import pytest
from unittest.mock import patch
import logging.config
from persephone_client import Persephone

# PROJECT IMPORTS
from decouple import Config, RepositoryEnv

# INTERNAL LIBS
from tests.src.stubs.bank_account_stubs.stub_get_account import (
    jwt_with_bank_account_to_create,
)
from src.services.bank_account.service import UserBankAccountService
from src.repositories.bank_account.repository import UserBankAccountRepository
from src.domain.exception import BadRequestError, InternalServerError, FailToSaveAuditingTrail

device_info_stub = {
                "device_name": "iphone",
                "device_model": "13",
                "is_emulator": True,
                "device_operating_system_name": "IOS",
                "os_sdk_version": "45125",
                "device_is_in_root_mode": True,
                "device_network_interfaces": "hahahaha",
                "public_ip": "1548455475221",
                "access_ip": "0000145455545",
                "phone_wifi_ip": "123255444456",
                "geolocation": "Brasil, São Paulo, SP",
            }


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
async def test_create_user_when_sending_the_right_params_then_return_the_duly_deleted_message(
    mock_existing_user_bank_account_and_is_activated,
    mock_save_registered_user_bank_accounts,
    mock_bank_code_from_client_exists,
    mock_send_to_persephone
):

    response = await UserBankAccountService.create_user_bank_accounts(
        bank_account_repository=UserBankAccountRepository,
        jwt_data=jwt_with_bank_account_to_create,
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
async def test_create_user_when_sending_the_right_params_but_account_is_from_user_and_account_is_already_activated(
        mock_existing_user_bank_account_and_is_activated,
        mock_save_registered_user_bank_accounts,
        mock_bank_code_from_client_exists,
        mock_send_to_persephone

):
    with pytest.raises(FailToSaveAuditingTrail):
        await UserBankAccountService.create_user_bank_accounts(
            jwt_data=jwt_with_bank_account_to_create,
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
async def test_when_sending_the_right_params_and_bank_account_is_not_activated_then_raise_fail_to_save(
        mock_send_to_persephone,
        mock_bank_code_from_client_exists,
        mock_save_registered_user_bank_accounts,
        mock_existing_user_bank_account_and_is_activated
):

    with pytest.raises(FailToSaveAuditingTrail):
        await UserBankAccountService.create_user_bank_accounts(
            jwt_data=jwt_with_bank_account_to_create,
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
async def test_create_user_when_sending_the_right_params_but_account_is_activated_and_saved(
        mock_send_to_persephone,
        mock_bank_code_from_client_exists,
        mock_save_registered_user_bank_accounts,
        mock_existing_user_bank_account_and_is_activated
):

    with pytest.raises(InternalServerError):
        await UserBankAccountService.create_user_bank_accounts(
            jwt_data=jwt_with_bank_account_to_create,
            bank_account_repository=UserBankAccountRepository,
        )


@pytest.mark.asyncio
async def test_when_sending_wrong_params_of_bank_account_repository_then_raise_attribute_error():
    with pytest.raises(AttributeError):
        await UserBankAccountService.create_user_bank_accounts(
            bank_account_repository=None, jwt_data=jwt_with_bank_account_to_create
        )


@pytest.mark.asyncio
async def test_when_jwt_data_payload_is_invalid_then_raise_type_error_as_expected():
    with pytest.raises(TypeError):
        await UserBankAccountService.create_user_bank_accounts(
            jwt_data=None, bank_account_repository=UserBankAccountRepository
        )
