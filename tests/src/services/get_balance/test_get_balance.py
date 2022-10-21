# Standard Libs
import pytest
from unittest.mock import patch

# External Libs
from src.domain.enums.region import Region
from src.domain.request.exchange_info.get_balance_validator import GetBalanceModel
from src.repositories.base_repositories.oracle.repository import OracleBaseRepository
from tests.src.stubs.project_stubs.stub_data import (
    payload_data_dummy,
    StubOracleRepository,
)

# @pytest.mark.asyncio
# @patch.object(Statement, "get_balance", return_value={"balance": 104993635.20})
# async def test_dw_balance_function_us_then_return_expected_and_balance_is_in_response(
#     mock_get_dw_balance,
# ):
#     response = await Statement.get_balance()
#     assert response == {"balance": 104993635.20}
#     assert response["balance"] == 104993635.20
#     assert isinstance(response, dict)
