# Standard Libs
import pytest
from unittest.mock import patch

# EXTERNAL LIBS
from src.repositories.base_repositories.mongo_db.base import MongoDbBaseRepository
from src.repositories.stock_portfolios.repository import StockPortfoliosRepository
from tests.src.stubs.bank_account_stubs.stub_get_account import stock_portfolios_response_dummy

portfolios_stub = {"portfolios": {"default": {"br": {
                "bovespa_account": "000000014-6",
                "bmf_account": "14"},
            "us": {
                "dw_id": "89c69304-018a-40b7-be5b-2121c16e109e",
                "dw_account": "89c69304-018a-40b7-be5b-2121c16e109e.1651525277006"
            }},
        "vnc": {"br": [{
                    "bovespa_account": "000000071-5",
                    "bmf_account": "71"
                },{
                    "bovespa_account": "000000018-9",
                    "bmf_account": "18"
                }]}}}


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "find_one", return_value=portfolios_stub)
async def test_when_sending_the_right_params_to_repository_then_return_the_expected(
        mock_find_one
):
    response = await StockPortfoliosRepository.get_stock_portfolios_accounts(
        unique_id="40db7fee-6d60-4d73-824f-1bf87edc4491"
    )
    assert response == stock_portfolios_response_dummy
    assert response.get("vnc_portfolios").get("br")[1].get("bmf_account") == "18"


@pytest.mark.asyncio
@patch.object(MongoDbBaseRepository, "find_one", return_value=None)
async def test_when_sending_the_right_params_to_repository_then_return_a_dict_with_an_empty_dictionary_value(
        mock_find_one
):
    response = await StockPortfoliosRepository.get_stock_portfolios_accounts(
        unique_id="40db7fee-6d60-4d73-824f-1bf87edc4491"
    )
    none_response = {"default": {},
                    "vnc_portfolios": {}}

    assert response == none_response
