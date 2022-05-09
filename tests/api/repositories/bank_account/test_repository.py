# # Standard Libs
# import pytest
# from unittest.mock import patch, MagicMock
# 
# # INTERNAL LIBS
# from api.repositories.bank_account.repository import UserBankAccountRepository
# from api.repositories.base_repositories.mongo_db.base import MongoDbBaseRepository
# from tests.stubs.bank_account_stubs.stub_get_account import get_accounts_dummy, find_all_response_dummy
#
#
# @pytest.mark.asyncio
# @patch.object(MongoDbBaseRepository, 'find_all', return_value=find_all_response_dummy)
# async def test_when_sending_the_right_params_to_registered_user_bank_account_then_return_true(mock_find_all):
#     response = await UserBankAccountRepository.get_registered_user_bank_accounts(unique_id="40db7fee-6d60-4d73-824f-1bf87edc4491")
#     assert response == True
