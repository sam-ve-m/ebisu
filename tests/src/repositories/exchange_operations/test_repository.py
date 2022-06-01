# STANDARD LIBS
import pytest
from unittest.mock import patch

# EXTERNAL LIBS
from src.repositories.base_repositories.mongo_db.base import MongoDbBaseRepository
from src.repositories.exchange_operations.repository import UserExchangeOperationsRepository
from tests.src.repositories.exchange_operations.stubs import exchange_template_stub


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "insert", return_value=True)
async def test_when_sending_the_right_params_then_return_the_expected_which_is_true(
        mock_insert
):
    response = await UserExchangeOperationsRepository.save_user_exchange_operations(
        exchange_template=exchange_template_stub
    )
    assert response == True


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "insert", return_value=False)
async def test_when_sending_the_right_params_then_return_the_expected_which_is_false(
        mock_insert
):
    response = await UserExchangeOperationsRepository.save_user_exchange_operations(
        exchange_template=None
    )
    assert response == False
