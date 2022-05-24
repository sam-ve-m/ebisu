# # Standard Libs
import pytest
from unittest.mock import patch

# INTERNAL LIBS
from src.repositories.bank_account.repository import UserBankAccountRepository
from src.repositories.base_repositories.mongo_db.base import MongoDbBaseRepository
from src.services.get_bank_code.service import GetBankCode
from tests.src.stubs.bank_account_stubs.stub_get_account import (
    find_all_response_dummy,
    find_one_response_dummy,
    find_one_wrong_response_dummy,
    user_from_client_stub,
    user_from_client_2_stub,
    find_one_response_with_cpf_dummy,
)

# stubs
account_repository_id_stub = "40db7fee-6d60-4d73-824f-1bf87edc4491"
bank_account_repository_stub = {"bank_account": "648498574893"}

bank_codes_valid_stub = [{"code": "070", "description": "BANCO REGIONAL DE BRASILIA"},
    {"code": "097", "description": "BEP - BANCO DO ESTADO DO PARANA S/A"}]

create_bank_account_stub = {"bank": "070", "account_type": "090948747654", "agency": "8776262563",
    "account_number": "9938373-2", "account_name": "corrente", "cpf":"58038116020"}

create_bank_account_invalid_stub = {"bank": "77265353572973", "account_type": "090948747654", "agency": "8776262563",
    "account_number": "9938373-2", "account_name": "corrente", "cpf":"58038116020"}


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

    assert response == None


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "add_one_in_array", return_value=True)
async def test_when_sending_valid_params_to_save_register_accounts_then_return_the_expected(
    mock_add_one_in_array,
):
    response = await UserBankAccountRepository.save_registered_user_bank_accounts(
        unique_id=account_repository_id_stub, bank_account=bank_account_repository_stub
    )
    assert response == True


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
    assert response == True


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
    assert response == False


@pytest.mark.asyncio
@patch.object(
    MongoDbBaseRepository, "find_one", return_value=existing_account_repository_stub
)
async def test_when_sending_the_right_params_to_is_bank_account_from_client_then_return_the_expected(
    mock_find_one,
):
    response = await UserBankAccountRepository.is_user_bank_account_from_client(
        unique_id=account_repository_id_stub, bank_account=user_from_client_stub
    )
    assert response == True


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "find_one", return_value=None)
async def test_when_sending_the_right_params_to_is_bank_account_from_client_then_return_false(
    mock_find_one,
):
    response = await UserBankAccountRepository.is_user_bank_account_from_client(
        unique_id=account_repository_id_stub, bank_account=user_from_client_2_stub
    )
    assert response == False


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
    assert response == True


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "find_one", return_value=None)
async def test_when_sending_the_right_params_to_account_id_exists_then_return_the_expected_which_is_false(
    mock_find_one,
):
    response = await UserBankAccountRepository.user_bank_account_id_exists(
        unique_id=account_repository_id_stub, bank_account_id=None
    )
    assert response == False


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "update_one", return_value=True)
async def test_when_sending_the_right_params_to_update_registered_bank_account_then_return_the_expected(
    mock_update_one,
):

    response = await UserBankAccountRepository.update_registered_user_bank_accounts(
        unique_id=account_repository_id_stub, bank_account=find_one_response_dummy
    )

    assert response == True


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "update_one", return_value=False)
async def test_when_sending_the_right_params_to_update_registered_bank_account_then_return_false(
    mock_update_one,
):

    response = await UserBankAccountRepository.update_registered_user_bank_accounts(
        unique_id=account_repository_id_stub, bank_account=find_one_response_dummy
    )

    assert response == False


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "update_one", return_value=True)
async def test_when_sending_the_right_params_to_update_registered_bank_account_then_return_false(
    mock_update_one,
):
    response = await UserBankAccountRepository.update_registered_user_bank_accounts(
        unique_id=account_repository_id_stub,
        bank_account=find_one_response_with_cpf_dummy,
    )

    assert response == True


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "update_one", return_value=True)
async def test_when_sending_the_right_params_to_delete_registered_bank_account_then_return_true(
    mock_update_one,
):
    response = await UserBankAccountRepository.delete_registered_user_bank_accounts(
        unique_id=account_repository_id_stub,
        bank_account=find_one_response_with_cpf_dummy,
    )

    assert response == True


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "update_one", return_value=False)
async def test_when_sending_the_right_params_to_delete_registered_bank_account_then_return_true(
    mock_update_one,
):
    response = await UserBankAccountRepository.delete_registered_user_bank_accounts(
        unique_id=account_repository_id_stub,
        bank_account=find_one_response_with_cpf_dummy,
    )

    assert response == False

@pytest.mark.asyncio
@patch.object(GetBankCode, 'get_service_response', return_value=bank_codes_valid_stub)
async def test_when_sending_right_params_to_bank_code_from_client_exists_then_return_true(
        mock_bank_codes_valid_stub
):
    response = await UserBankAccountRepository.bank_code_from_client_exists(
        bank_account=create_bank_account_stub
    )
    assert response == True


@pytest.mark.asyncio
@patch.object(GetBankCode, 'get_service_response', return_value=bank_codes_valid_stub)
async def test_when_sending_right_params_to_bank_code_from_client_exists_then_return_true(
        mock_bank_codes_valid_stub
):
    response = await UserBankAccountRepository.bank_code_from_client_exists(
        bank_account=create_bank_account_invalid_stub
    )
    assert response == False