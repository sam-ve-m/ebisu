# Standard Libs
import pytest
from unittest.mock import patch

# EXTERNAL LIBS
from src.repositories.stock_portfolios.repository import StockPortfoliosRepository
from src.services.stock_portfolios_list.service import StockPortfoliosList
from tests.src.stubs.bank_account_stubs.stub_get_account import stock_portfolios_response_dummy, jwt_data_dummy


@pytest.mark.asyncio
@patch.object(StockPortfoliosRepository, "get_stock_portfolios_accounts", return_value=stock_portfolios_response_dummy)
async def test_when_sending_the_right_params_to_stock_portfolios_service_then_return_the_expected(
        mock_get_stock_portfolios_accounts
):
    response = await StockPortfoliosList.get_stock_portfolios_response(
        jwt_data=jwt_data_dummy, portfolios_repository=StockPortfoliosRepository
    )
    assert response == stock_portfolios_response_dummy
    assert response.get("default").get("br").get("bmf_account") == "14"


@pytest.mark.asyncio
@patch.object(
    StockPortfoliosRepository, "get_stock_portfolios_accounts", return_value={"default": {}, "vnc_portfolios": {}}
)
async def test_when_sending_the_right_params_to_portfolios_service_then_return_the_an_empty_list(
        mock_get_stock_portfolios_accounts
):
    response = await StockPortfoliosList.get_stock_portfolios_response(
        jwt_data=jwt_data_dummy, portfolios_repository=StockPortfoliosRepository
    )
    empty_portfolio = {"default": {}, "vnc_portfolios": {}}

    assert response == empty_portfolio
    assert isinstance(response, dict)
