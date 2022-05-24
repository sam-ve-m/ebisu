# Standard Libs
import pytest
from unittest.mock import patch

# EXTERNAL LIBS
from src.domain.validators.stock_portfolios.validators import UserPortfoliosModel
from src.repositories.user_portfolios.repository import UserPortfoliosRepository
from src.services.stock_portfolios_list.service import UserPortfoliosList
from tests.src.stubs.bank_account_stubs.stub_get_account import stock_portfolios_response_dummy, jwt_data_dummy


# stubs
all_portfolios_stub = {"default": {"br": {"bovespa_account": "000000014-6",
            "bmf_account": "14"}, "us": {"dw_id": "89c69304-018a-40b7-be5b-2121c16e109e",
            "dw_account": "89c69304-018a-40b7-be5b-2121c16e109e.1651525277006"
        }}, "vnc_portfolios": {"br": [{"bovespa_account": "000000071-5", "bmf_account": "71"},
            {"bovespa_account": "000000018-9", "bmf_account": "18"}]}}

classification_type_stub = {"vnc": {"br": [{"bovespa_account": "000000071-5",
                "bmf_account": "71"},{"bovespa_account": "000000018-9","bmf_account": "18"
            }]}}

portfolios_by_region_stub = {"default": {"br": {"bovespa_account": "000000014-6", "bmf_account": "14"
        }}, "vnc_portfolios": {"br": [{"bovespa_account": "000000071-5","bmf_account": "71"
            },{"bovespa_account": "000000018-9","bmf_account": "18"}]}}

port_class_and_region_stub = {"br": [{"bovespa_account": "000000071-5","bmf_account": "71"
        },{"bovespa_account": "000000018-9","bmf_account": "18"}]}

unique_id_stub = "40db7fee-6d60-4d73-824f-1bf87edc4491"


@pytest.mark.asyncio
@patch.object(UserPortfoliosRepository, 'get_all_portfolios_list', return_value=all_portfolios_stub)
async def test_when_sending_the_right_params_to_get_all_stock_portfolios_list_function_then_return_the_expected(
        mock_get_all_portfolios_list
):

    response = await UserPortfoliosList.get_all_stock_portfolios_list(
        unique_id=unique_id_stub, portfolios_repository=UserPortfoliosRepository
    )
    assert response == all_portfolios_stub


@pytest.mark.asyncio
@patch.object(UserPortfoliosRepository, 'get_portfolios_by_type', return_value=classification_type_stub)
async def test_when_get_portfolios_by_type_of_classification_params_are_correct_then_return_the_expected(
        mock_get_portfolios_by_type
):
    response = await UserPortfoliosList.get_portfolios_by_type_of_classification(
        portfolios_repository=UserPortfoliosRepository,
        unique_id=unique_id_stub,
        user_portfolios=UserPortfoliosModel(**{
            "portfolio_classification": "VNC"
        })
    )
    assert response == classification_type_stub


@pytest.mark.asyncio
@patch.object(UserPortfoliosRepository, 'get_portfolios_by_region', return_value=portfolios_by_region_stub)
async def test_when_sending_params_to_get_portfolios_by_region_br_or_us_then_return_expected(
        mock_get_portfolios_by_region
):
    response = await UserPortfoliosList.get_portfolios_by_region_br_or_us(
        portfolios_repository=UserPortfoliosRepository,
        unique_id=unique_id_stub,
        user_portfolios=UserPortfoliosModel(**{
            "region": "BR"
        })
    )
    assert response == portfolios_by_region_stub


@pytest.mark.asyncio
@patch.object(UserPortfoliosRepository,
              'get_portfolios_by_type_and_region',
              return_value=port_class_and_region_stub)
async def test_when_sending_right_params_to_get_portfolios_by_type_classification_and_region_then_return_the_expected(
        mock_get_portfolios_by_type_classification_and_region
):
    response = await UserPortfoliosList.get_portfolios_by_type_classification_and_region(
        portfolios_repository=UserPortfoliosRepository,
        unique_id=unique_id_stub,
        user_portfolios=UserPortfoliosModel(**{
            "region": "BR",
            "portfolio_classification": "VNC"
        })
    )
    assert response == port_class_and_region_stub


@pytest.mark.asyncio
@patch.object(UserPortfoliosList, "get_all_stock_portfolios_list", return_value=stock_portfolios_response_dummy)
async def test_when_sending_the_right_params_to_stock_portfolios_service_then_return_the_expected(
        mock_get_stock_portfolios_accounts
):
    response = await UserPortfoliosList.get_user_portfolios_response(
        jwt_data=jwt_data_dummy,
        portfolios_repository=UserPortfoliosRepository,
        user_portfolios=UserPortfoliosModel(**{})
    )
    assert response == stock_portfolios_response_dummy


@pytest.mark.asyncio
@patch.object(
    UserPortfoliosList, "get_all_stock_portfolios_list", return_value={"default": {}, "vnc_portfolios": {}}
)
async def test_when_sending_the_right_params_to_portfolios_service_then_return_the_an_empty_list(
        mock_get_stock_portfolios_accounts
):
    response = await UserPortfoliosList.get_user_portfolios_response(
        jwt_data=jwt_data_dummy,
        portfolios_repository=UserPortfoliosRepository,
        user_portfolios=UserPortfoliosModel(**{})
    )
    empty_portfolio = {"default": {}, "vnc_portfolios": {}}

    assert response == empty_portfolio
    assert isinstance(response, dict)
