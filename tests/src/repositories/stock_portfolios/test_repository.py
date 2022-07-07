# Standard Libs
import pytest
from unittest.mock import patch
import logging.config

# PROJECT IMPORTS
from decouple import Config, RepositoryEnv
with patch.object(Config, "get", return_value="info"):
    with patch.object(logging.config, "dictConfig"):
        with patch.object(RepositoryEnv, "__init__", return_value=None):
            from src.repositories.base_repositories.mongo_db.base import MongoDbBaseRepository
            from src.repositories.user_portfolios.repository import UserPortfoliosRepository

# STUB IMPORTS
from tests.src.repositories.stock_portfolios.stub import (
    find_one_response_stub,
    unique_id_stub,
    find_one_by_type_stub,
)


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


find_one_region_stub = {
    "portfolios": {
        "default": {"br": {"bovespa_account": "000000014-6", "bmf_account": "14"}},
        "vnc": {
            "br": [
                {"bovespa_account": "000000071-5", "bmf_account": "71"},
                {"bovespa_account": "000000018-9", "bmf_account": "18"},
            ]
        },
    }
}


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "find_one", return_value=find_one_region_stub)
async def test_when_sending_the_right_params_to_get_portfolios_by_region_then_return_the_expected(
    mock_find_one,
):
    response = await UserPortfoliosRepository.get_portfolios_by_region(
        unique_id=unique_id_stub, region="BR"
    )

    assert response == find_one_region_stub.get("portfolios")


response_portfolios_stub = {"portfolios": {"default": {}, "vnc": {}}}


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "find_one", return_value=response_portfolios_stub)
async def test_when_sending_the_right_params_to_get_portfolios_by_region_then_return_no_data_which_is_the_expected(
    mock_find_one,
):
    response = await UserPortfoliosRepository.get_portfolios_by_region(
        unique_id=unique_id_stub, region="BR"
    )

    assert response == {"default": {}, "vnc": {}}


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "find_one", return_value=find_one_by_type_stub)
async def test_when_sending_the_right_params_to_get_portfolios_by_type_then_return_the_expected(
    mock_find_one,
):
    response = await UserPortfoliosRepository.get_portfolios_by_type(
        unique_id=unique_id_stub, portfolio_classification="VNC"
    )

    assert response == find_one_by_type_stub.get("portfolios")


find_one_type_stub = {"portfolios": {"vnc": {}}}


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "find_one", return_value=find_one_type_stub)
async def test_when_sending_the_right_params_to_portfolios_by_type_then_return_no_data_response(
    mock_find_one,
):
    response = await UserPortfoliosRepository.get_portfolios_by_type(
        unique_id=unique_id_stub, portfolio_classification="VNC"
    )

    assert response == {"vnc": {}}


find_one_type_and_class_stub = {"portfolios": {"vnc": {}}}


@pytest.mark.asyncio
@patch.object(
    MongoDbBaseRepository, "find_one", return_value=find_one_type_and_class_stub
)
async def test_when_sending_the_right_params_to_portfolios_by_type_and_region_then_return_no_data_response(
    mock_find_one,
):
    response = await UserPortfoliosRepository.get_portfolios_by_type_and_region(
        unique_id=unique_id_stub, portfolio_classification="VNC", region="BR"
    )
    assert response == {"vnc": {}}


find_type_and_class_stub = {
    "portfolios": {
        "default": {"br": {"bovespa_account": "000000014-6", "bmf_account": "14"}}
    }
}
find_stub_by_type_and_region = {
    "default": {"br": {"bovespa_account": "000000014-6", "bmf_account": "14"}}
}


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "find_one", return_value=find_type_and_class_stub)
async def test_when_sending_the_right_params_to_type_and_region_then_return_the_expected(
    mock_find_one,
):
    response = await UserPortfoliosRepository.get_portfolios_by_type_and_region(
        unique_id=unique_id_stub, portfolio_classification="DEFAULT", region="BR"
    )
    assert response == find_stub_by_type_and_region
