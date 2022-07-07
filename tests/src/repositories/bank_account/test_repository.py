# STANDARD LIBS
import pytest
from unittest.mock import patch
import logging.config

# INTERNAL LIBS
from decouple import Config, RepositoryEnv
with patch.object(Config, "get", return_value="info"):
    with patch.object(logging.config, "dictConfig"):
        with patch.object(RepositoryEnv, "__init__", return_value=None):
            from src.repositories.bank_account.repository import UserBankAccountRepository
            from src.repositories.base_repositories.mongo_db.base import MongoDbBaseRepository
            from src.services.bank_account.service import UserBankAccountService
            from src.services.get_bank_code.service import GetBankCode

# STUB IMPORTS
from tests.src.repositories.bank_account.stubs import (
    account_repository_id_stub,
    bank_account_repository_stub,
    bank_codes_valid_stub,
)
from tests.src.stubs.bank_account_stubs.stub_get_account import (
    find_all_response_dummy,
    find_one_response_dummy,
    find_one_wrong_response_dummy,
    user_from_client_stub,
    user_from_client_2_stub,
    find_one_response_with_cpf_dummy,
)


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "find_all", return_value=find_all_response_dummy)
async def test_when_sending_the_right_params_to_registered_user_bank_account_then_return_the_expected_response(
    mock_find_all,
):
    response = await UserBankAccountRepository.get_registered_user_bank_accounts(
        unique_id=account_repository_id_stub
    )

    assert response == find_all_response_dummy[0]


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "find_all", return_value=None)
async def test_when_sending_the_right_params_to_registered_user_bank_account_then_return_none(
    mock_find_all,
):
    response = await UserBankAccountRepository.get_registered_user_bank_accounts(
        unique_id=account_repository_id_stub
    )

    assert response is None


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "add_one_in_array", return_value=True)
async def test_when_sending_valid_params_to_save_register_accounts_then_return_the_expected(
    mock_add_one_in_array,
):
    response = await UserBankAccountRepository.save_registered_user_bank_accounts(
        unique_id=account_repository_id_stub, bank_account=bank_account_repository_stub
    )
    assert response is True


existing_account_repository_stub = {"bank_account": "648498574893"}
existing_account_repository_2_stub = {"bank_account": None}


@pytest.mark.asyncio
@patch.object(
    MongoDbBaseRepository, "find_one", return_value=existing_account_repository_stub
)
async def test_when_sending_the_right_params_then_return_the_expect_which_is_true(
    mock_find_one,
):
    response = (
        await UserBankAccountRepository.existing_user_bank_account_and_is_activated(
            unique_id=account_repository_id_stub, bank_account=find_one_response_dummy
        )
    )
    assert response is True


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "find_one", return_value=None)
async def test_when_sending_the_right_params_then_return_the_expect_which_is_false(
    mock_find_one,
):
    response = (
        await UserBankAccountRepository.existing_user_bank_account_and_is_activated(
            unique_id=account_repository_id_stub,
            bank_account=find_one_wrong_response_dummy,
        )
    )
    assert response is False



@pytest.mark.asyncio
@patch.object(
    MongoDbBaseRepository, "find_one", return_value=existing_account_repository_stub
)
async def test_when_sending_the_right_params_to_account_id_exists_then_return_the_expected_which_is_true(
    mock_find_one,
):
    response = await UserBankAccountRepository.user_bank_account_id_exists(
        unique_id=account_repository_id_stub, bank_account_id="99927276253-2"
    )
    assert response is True


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "find_one", return_value=None)
async def test_when_sending_the_right_params_to_account_id_exists_then_return_the_expected_which_is_false(
    mock_find_one,
):
    response = await UserBankAccountRepository.user_bank_account_id_exists(
        unique_id=account_repository_id_stub, bank_account_id=None
    )
    assert response is False


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "update_one", return_value=True)
async def test_when_sending_the_right_params_to_update_registered_bank_account_then_return_the_expected(
    mock_update_one,
):
    response = await UserBankAccountRepository.update_registered_user_bank_accounts(
        unique_id=account_repository_id_stub, bank_account=find_one_response_dummy
    )

    assert response is True


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "update_one", return_value=False)
async def test_when_sending_the_right_params_to_update_registered_bank_account_then_return_false(
    mock_update_one,
):
    response = await UserBankAccountRepository.update_registered_user_bank_accounts(
        unique_id=account_repository_id_stub, bank_account=find_one_response_dummy
    )

    assert response is False


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "update_one", return_value=True)
async def test_when_sending_the_right_params_to_update_registered_bank_account_then_return_false(
    mock_update_one,
):
    response = await UserBankAccountRepository.update_registered_user_bank_accounts(
        unique_id=account_repository_id_stub,
        bank_account=find_one_response_with_cpf_dummy,
    )

    assert response is True


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "update_one", return_value=True)
async def test_when_sending_the_right_params_to_delete_registered_bank_account_then_return_true(
    mock_update_one,
):
    response = await UserBankAccountRepository.delete_registered_user_bank_accounts(
        unique_id=account_repository_id_stub,
        bank_account=find_one_response_with_cpf_dummy,
    )

    assert response is True


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "update_one", return_value=False)
async def test_when_sending_the_right_params_to_delete_registered_bank_account_then_return_true(
    mock_update_one,
):
    response = await UserBankAccountRepository.delete_registered_user_bank_accounts(
        unique_id=account_repository_id_stub,
        bank_account=find_one_response_with_cpf_dummy,
    )

    assert response is False


@patch.object(GetBankCode, "get_bank_code_from_database", return_value="070")
def test_when_sending_right_params_to_bank_code_from_client_exists_then_return_true(
    mock_get_service_response,
):
    response = UserBankAccountService.bank_code_from_client_exists(bank="070")
    assert response is True


@patch.object(GetBankCode, "get_service_response", return_value=bank_codes_valid_stub)
def test_when_sending_invalid_params_to_bank_code_from_client_exists_then_return_true(
    mock_get_service_response,
):
    response = UserBankAccountService.bank_code_from_client_exists(
        bank="123456"
    )
    assert response == False


find_one_stub = {"name": "Teste Teste", "identifier_document": {"cpf": "40340423410"}}


# test get_cpf_and_name_from_user
@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "find_one", return_value=find_one_stub)
async def test_when_sending_right_params_then_return_the_expected(mock_find_one):
    response = await UserBankAccountRepository.get_cpf_and_name_from_user(
        unique_id="1384f391-ceb6-444b-b649-db55cbcc0f9f"
    )
    assert response == ("Teste Teste", "40340423410")
