# STANDARD LIBS
import pytest
from unittest.mock import patch

# EXTERNAL LIBS
from src.repositories.base_repositories.mongo_db.base import MongoDbBaseRepository
from src.repositories.exchange_operations.repository import UserExchangeOperationsRepository
from src.services.exchange_operations.services import ExchangeOperationsService
from tests.src.stubs.project_stubs.stub_data import payload_data_resume, resume_obj

cpf_and_name = {'cpf': '40340423410', 'name': 'Teste Teste'}

@patch.object(MongoDbBaseRepository, "find_one", return_value=cpf_and_name)
@patch.object(UserExchangeOperationsRepository, "insert", return_value=True)
@pytest.mark.asyncio
async def test_get_service_response_to_save_exchange_operations_when_sending_right_params_then_return_the_expected(
    mock_find_one, mock_insert
):
    response = ExchangeOperationsService.get_service_response_to_save_exchange_operations(
        jwt_data=payload_data_resume, resume=resume_obj
    )
    assert response == True
