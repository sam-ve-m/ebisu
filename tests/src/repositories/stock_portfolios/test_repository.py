# Standard Libs
import pytest
from unittest.mock import patch

# EXTERNAL LIBS
from src.repositories.base_repositories.mongo_db.base import MongoDbBaseRepository
from src.repositories.user_portfolios.repository import UserPortfoliosRepository
from tests.src.repositories.stock_portfolios.stub import find_one_response_stub, unique_id_stub, \
    find_one_by_region_stub, find_one_by_type_stub, find_one_by_type_and_region


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "find_one", return_value=find_one_response_stub)
async def test_when_sending_the_right_params_to_get_all_portfolios_list_then_return_the_expected(
    mock_find_one,
):
    response = await UserPortfoliosRepository.get_all_portfolios_list(
        unique_id=unique_id_stub
    )
    assert response == find_one_response_stub.get("portfolios")
    assert isinstance(response, dict)


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "find_one", return_value=None)
async def test_when_sending_the_right_params_to_get_all_portfolios_list_then_return_the_expected_for_no_data(
    mock_find_one,
):
    response = await UserPortfoliosRepository.get_all_portfolios_list(
        unique_id=unique_id_stub
    )
    assert response == {"default": {}, "vnc_portfolios": {}}


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "find_one", return_value=find_one_by_region_stub)
async def test_when_sending_the_right_params_to_get_portfolios_by_region_then_return_the_expected(
    mock_find_one,
):
    response = await UserPortfoliosRepository.get_portfolios_by_region(
        unique_id=unique_id_stub, region="BR"
    )

    assert response == find_one_by_region_stub.get("portfolios")


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "find_one", return_value=None)
async def test_when_sending_the_right_params_to_get_portfolios_by_region_then_return_no_data_which_is_the_expected(
    mock_find_one,
):
    response = await UserPortfoliosRepository.get_portfolios_by_region(
        unique_id=unique_id_stub, region="BR"
    )

    assert response == {"default": {}, "vnc_portfolios": {}}


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "find_one", return_value=find_one_by_type_stub)
async def test_when_sending_the_right_params_to_get_portfolios_by_type_then_return_the_expected(
    mock_find_one,
):
    response = await UserPortfoliosRepository.get_portfolios_by_type(
        unique_id=unique_id_stub, portfolio_classification="VNC"
    )

    assert response == find_one_by_type_stub.get("portfolios")


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "find_one", return_value=None)
async def test_when_sending_the_right_params_to_portfolios_by_type_then_return_no_data_response(
    mock_find_one,
):
    response = await UserPortfoliosRepository.get_portfolios_by_type(
        unique_id=unique_id_stub, portfolio_classification="VNC"
    )

    assert response == {"vnc": {}}


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "find_one", return_value=None)
async def test_when_sending_the_right_params_to_portfolios_by_type_and_region_then_return_no_data_response(
    mock_find_one,
):
    response = await UserPortfoliosRepository.get_portfolios_by_type_and_region(
        unique_id=unique_id_stub, portfolio_classification="VNC", region="BR"
    )
    assert response == {"vnc": {}}


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "find_one", return_value=find_one_by_type_stub)
async def test_when_sending_the_right_params_to_type_and_region_then_return_the_expected(
    mock_find_one,
):
    response = await UserPortfoliosRepository.get_portfolios_by_type_and_region(
        unique_id=unique_id_stub, portfolio_classification="VNC", region="BR"
    )
    assert response == {'vnc': find_one_by_type_and_region}
