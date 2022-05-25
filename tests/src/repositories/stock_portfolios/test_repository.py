# Standard Libs
import pytest
from unittest.mock import patch

# EXTERNAL LIBS
from src.repositories.base_repositories.mongo_db.base import MongoDbBaseRepository
from src.repositories.user_portfolios.repository import UserPortfoliosRepository


unique_id_stub = "40db7fee-6d60-4d73-824f-1bf87edc4491"

find_one_response_stub = {"portfolios": {"default": {"br": {"bovespa_account": "000000014-6","bmf_account": "14"},
            "us": {"dw_id": "89c69304-018a-40b7-be5b-2121c16e109e", "dw_account": "89c69304-018a-40b7-be5b-2121c16e109e.1651525277006"
            }},"vnc": {"br": [{"bovespa_account": "000000071-5","bmf_account": "71"
                },{ "bovespa_account": "000000018-9",
                    "bmf_account": "18"}]}}}

find_one_by_region_stub = {'portfolios': {'default': {'br': {'bovespa_account': '000000014-6', 'bmf_account': '14'}}, 'vnc': {'br': [{'bovespa_account': '000000071-5', 'bmf_account': '71'}, {'bovespa_account': '000000018-9', 'bmf_account': '18'}]}}}

find_one_by_type_stub = {'portfolios': {'vnc': {'br': [{'bovespa_account': '000000071-5', 'bmf_account': '71'}, {'bovespa_account': '000000018-9', 'bmf_account': '18'}]}}}

find_one_by_type_and_region = {"br": [{"bovespa_account": "000000071-5","bmf_account": "71"},
        {"bovespa_account": "000000018-9","bmf_account": "18"}]}


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "find_one", return_value=find_one_response_stub)
async def test_when_sending_the_right_params_to_get_all_portfolios_list_then_return_the_expected(
        mock_find_one
):
    response = await UserPortfoliosRepository.get_all_portfolios_list(
        unique_id=unique_id_stub
    )
    assert response == find_one_response_stub.get("portfolios")
    assert isinstance(response, dict)


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "find_one", return_value=None)
async def test_when_sending_the_right_params_to_get_all_portfolios_list_then_return_the_expected_for_no_data(
        mock_find_one
):
    response = await UserPortfoliosRepository.get_all_portfolios_list(
        unique_id=unique_id_stub
    )
    assert response == {"default": {}, "vnc_portfolios": {}}


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "find_one", return_value=find_one_by_region_stub)
async def test_when_sending_the_right_params_to_get_portfolios_by_region_then_return_the_expected(
        mock_find_one
):
    response = await UserPortfoliosRepository.get_portfolios_by_region(
        unique_id=unique_id_stub, region="BR"
    )

    assert response == find_one_by_region_stub.get("portfolios")


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "find_one", return_value=None)
async def test_when_sending_the_right_params_to_get_portfolios_by_region_then_return_no_data_which_is_the_expected(
            mock_find_one
):
    response = await UserPortfoliosRepository.get_portfolios_by_region(
        unique_id=unique_id_stub, region="BR"
    )

    assert response == {"default": {}, "vnc_portfolios": {}}


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "find_one", return_value=find_one_by_type_stub)
async def test_when_sending_the_right_params_to_get_portfolios_by_type_then_return_the_expected(
            mock_find_one
):
    response = await UserPortfoliosRepository.get_portfolios_by_type(
        unique_id=unique_id_stub, portfolio_classification="VNC"
    )

    assert response == find_one_by_type_stub.get("portfolios")


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "find_one", return_value=None)
async def test_when_sending_the_right_params_to_portfolios_by_type_then_return_no_data_response(
        mock_find_one
):
    response = await UserPortfoliosRepository.get_portfolios_by_type(
        unique_id=unique_id_stub, portfolio_classification="VNC"
    )

    assert response == {"vnc": {}}


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "find_one", return_value=None)
async def test_when_sending_the_right_params_to_portfolios_by_type_and_region_then_return_no_data_response(
        mock_find_one
):
    response = await UserPortfoliosRepository.get_portfolios_by_type_and_region(
        unique_id=unique_id_stub, portfolio_classification="VNC", region="BR"
    )
    assert response == {"vnc": {}}


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "find_one", return_value=find_one_by_type_stub)
async def test_when_sending_the_right_params_to_type_and_region_then_return_the_expected(
mock_find_one
):
    response = await UserPortfoliosRepository.get_portfolios_by_type_and_region(
        unique_id=unique_id_stub, portfolio_classification="VNC", region="BR"
    )
    assert response == {'vnc': find_one_by_type_and_region}
