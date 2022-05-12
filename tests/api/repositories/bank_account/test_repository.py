# # Standard Libs
import pytest
from unittest.mock import patch, MagicMock

# INTERNAL LIBS
from api.repositories.bank_account.repository import UserBankAccountRepository
from api.repositories.base_repositories.mongo_db.base import MongoDbBaseRepository
from tests.api.stubs.bank_account_stubs.stub_get_account import find_all_response_dummy, find_one_response_dummy, \
    request_bank_account_dummy

# stubs
account_repository_id_stub = "40db7fee-6d60-4d73-824f-1bf87edc4491"
bank_account_repository_stub = {"bank_account": "648498574893"}

@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, 'find_all', return_value=find_all_response_dummy)
async def test_when_sending_the_right_params_to_registered_user_bank_account_then_return_the_expected_response(
        mock_find_all):

    response = await UserBankAccountRepository.get_registered_user_bank_accounts(
        unique_id=account_repository_id_stub)

    assert response == find_all_response_dummy[0]


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, 'find_all', return_value=None)
async def test_when_sending_the_right_params_to_registered_user_bank_account_then_return_none(
        mock_find_all):

    response = await UserBankAccountRepository.get_registered_user_bank_accounts(
        unique_id=account_repository_id_stub)

    assert response == None


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, 'add_one_in_array', return_value=True)
async def test_when_sending_valid_params_to_save_register_accounts_then_return_the_expected(mock_add_one_in_array):
    response = await UserBankAccountRepository.save_registered_user_bank_accounts(
        unique_id=account_repository_id_stub,
        bank_account=bank_account_repository_stub
    )
    assert response == True


existing_account_repository_stub = {"bank_account": "648498574893"}

# existing_user_bank_account_and_is_activated function wasn't tested
# @pytest.mark.asyncio
# @patch.object(MongoDbBaseRepository, "find_one", return_value=existing_account_repository_stub)
# async def test_when_sending_the_right_params_then_return_the_expect_which_is_true(mock_find_one):
#     response = await UserBankAccountRepository.existing_user_bank_account_and_is_activated(
#         unique_id=account_repository_id_stub,
#         bank_account=find_one_response_dummy
#     )
#     assert response == True
