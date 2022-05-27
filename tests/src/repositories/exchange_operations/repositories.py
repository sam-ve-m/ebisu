import pytest
from unittest.mock import patch

from src.repositories.bank_account.repository import UserBankAccountRepository
from src.repositories.base_repositories.mongo_db.base import MongoDbBaseRepository
from src.repositories.exchange_operations.repository import UserExchangeOperationsRepository
from tests.src.stubs.project_stubs.stub_data import payload_data_resume, resume_obj

cpf_and_name = {'cpf': '40340423410', 'name': 'Teste Teste'}

@pytest.mark.asyncio
@patch.object(UserBankAccountRepository, "get_cpf_and_name_from_user", return_value=cpf_and_name)
@patch.object(MongoDbBaseRepository, "insert", return_value=True)
async def test_when_sending_the_right_params_then_return_the_expected_which_is_true(
        mock_get_cpf_and_name_from_user, mock_insert
):
    response = await UserExchangeOperationsRepository.save_user_exchange_operations(
        jwt_data=payload_data_resume, resume=resume_obj
    )
    assert response == True

@pytest.mark.asyncio
@patch.object(UserBankAccountRepository, "get_cpf_and_name_from_user", return_value=cpf_and_name)
@patch.object(MongoDbBaseRepository, "insert", return_value=False)
async def test_when_sending_the_right_params_then_return_the_expected_which_is_false(
        mock_get_cpf_and_name_from_user, mock_insert
):
    response = await UserExchangeOperationsRepository.save_user_exchange_operations(
        jwt_data=payload_data_resume, resume=resume_obj
    )
    assert response == False
