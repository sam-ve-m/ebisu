# Standard Libs
import pytest
from unittest.mock import patch

# INTERNAL LIBS
from tests.src.stubs.bank_account_stubs.stub_get_account import (
    jwt_with_bank_account_to_delete,
)
from src.services.bank_account.service import UserBankAccountService
from src.repositories.bank_account.repository import UserBankAccountRepository
from src.domain.exception import BadRequestError, InternalServerError, FailToSaveAuditingTrail
from tests.src.stubs.project_stubs.stub_data import payload_data_dummy
from persephone_client import Persephone


@pytest.mark.asyncio
@patch.object(
    UserBankAccountRepository, "user_bank_account_id_exists", return_value=True
)
@patch.object(
    UserBankAccountRepository, "delete_registered_user_bank_accounts", return_value=True
)
async def test_delete_user_when_sending_the_right_params_then_return_the_duly_updated_message(
    mock_get_registered_user_bank_accounts, mock_delete_registered_user_bank_accounts
):

    response = await UserBankAccountService.delete_user_bank_account(
        jwt_data=jwt_with_bank_account_to_delete,
        bank_account_repository=UserBankAccountRepository,
    )
    dully_deleted_response = {"message": "Deleted"}

    assert response == dully_deleted_response
    assert isinstance(response, dict)
    assert response.get("message") == "Deleted"


@pytest.mark.asyncio
async def test_delete_user_when_sending_an_invalid_jwt_data_then_return_the_expected_exception():
    with pytest.raises(KeyError):
        await UserBankAccountService.delete_user_bank_account(
            jwt_data=payload_data_dummy,
            bank_account_repository=UserBankAccountRepository,
        )


@pytest.mark.asyncio
async def test_delete_user_when_sending_an_invalid_bank_repository_call_then_return_the_expected_attribute_exception():
    with pytest.raises(AttributeError):
        await UserBankAccountService.delete_user_bank_account(
            jwt_data=jwt_with_bank_account_to_delete, bank_account_repository=""
        )


@pytest.mark.asyncio
@patch.object(
    UserBankAccountRepository, "user_bank_account_id_exists", return_value=False
)
@patch.object(
    UserBankAccountRepository,
    "delete_registered_user_bank_accounts",
    return_value=False,
)
@patch.object(Persephone, "send_to_persephone", return_value=[False, False])
async def test_when_bank_account_and_register_account_are_false_then_raise_fail_to_delete_error(
    mock_get_registered_user_bank_accounts, mock_update_registered_user_bank_accounts, mock_send_to_persephone
):

    with pytest.raises(BadRequestError):
        await UserBankAccountService.delete_user_bank_account(
            jwt_data=jwt_with_bank_account_to_delete,
            bank_account_repository=UserBankAccountRepository,
        )


@pytest.mark.asyncio
@patch.object(
    UserBankAccountRepository, "user_bank_account_id_exists", return_value=True
)
@patch.object(
    UserBankAccountRepository,
    "delete_registered_user_bank_accounts",
    return_value=False,
)
@patch.object(Persephone, "send_to_persephone", return_value=[False, False])
async def test_when_register_account_is_false_then_raise_the_expected_fail_to_save_auditing_error(
    mock_get_registered_user_bank_accounts,
    mock_update_registered_user_bank_accounts,
    mock_send_to_persephone
):

    with pytest.raises(FailToSaveAuditingTrail):
        await UserBankAccountService.delete_user_bank_account(
            jwt_data=jwt_with_bank_account_to_delete,
            bank_account_repository=UserBankAccountRepository,
        )


@pytest.mark.asyncio
async def test_when_sending_wrong_params_of_user_bank_repository_then_raise_non_type_error():
    with pytest.raises(AttributeError):
        await UserBankAccountService.delete_user_bank_account(
            bank_account_repository="", jwt_data=jwt_with_bank_account_to_delete
        )


@pytest.mark.asyncio
async def test_when_jwt_data_is_not_valid_then_raise_type_error():
    with pytest.raises(TypeError):
        response = await UserBankAccountService.delete_user_bank_account(
            jwt_data=None, bank_account_repository=UserBankAccountRepository
        )
        assert response == "string indices must be integers"
