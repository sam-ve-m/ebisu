from unittest.mock import patch

from pytest import mark

from src.domain.earning.us.response.model import EarningsRecordResponse
from src.domain.enums.region import Region
from src.domain.validators.exchange_info.get_closure_steps_validator import (
    AccountCloseStepsRequest,
)
from src.repositories.user_portfolios.repository import UserPortfoliosRepository
from src.services.closure_steps.service import AccountCloseStepsService
from src.services.earnings_from_client.get_earnings_from_client import (
    EarningsFromClient,
)
from src.services.user_positions.service import UserPositionsService

user_portifolios_dummy = {
    "default": {
        "br": {
            "bovespa_account": "001",
            "created_at": "2022-01-01T03:00:00",
            "bmf_account": "1",
        },
        "us": {
            "dw_id": "123",
            "created_at": "2022-06-20T13:18:57.626000",
            "dw_account": "123",
            "dw_display_account": "LXSZ000123",
        },
    },
    "vnc": {
        "br": [
            {
                "bovespa_account": "002",
                "created_at": "2022-01-01T03:00:00",
                "bmf_account": "2",
            },
            {
                "bovespa_account": "003",
                "created_at": "2022-01-01T03:00:00",
                "bmf_account": "3",
            },
        ]
    },
}
jwt_data_dummy = {
    "exp": 1679011271,
    "created_at": 1647475271.217852,
    "scope": {
        "view_type": "default",
        "user_level": "client",
        "features": ["default", "realtime"],
    },
    "user": {
        "unique_id": "ID",
        "nick_name": "nick",
        "portfolios": {
            "br": {"bovespa_account": "1", "bmf_account": "1"},
            "us": {"_": None},
        },
        "client_has_br_trade_allowed": False,
        "client_has_us_trade_allowed": False,
        "client_profile": "investor",
    },
}


@mark.asyncio
@patch.object(UserPortfoliosRepository, "get_portfolios_by_region")
async def test_get_user_accounts_br(get_portfolios_by_region_mock):
    get_portfolios_by_region_mock.return_value = user_portifolios_dummy
    result = await AccountCloseStepsService._get_user_accounts(
        Region.BR.value, jwt_data_dummy
    )
    assert result == ["1", "2", "3"]


@mark.asyncio
@patch.object(UserPortfoliosRepository, "get_portfolios_by_region")
async def test_get_user_accounts_us(get_portfolios_by_region_mock):
    get_portfolios_by_region_mock.return_value = user_portifolios_dummy
    result = await AccountCloseStepsService._get_user_accounts(
        Region.US.value, jwt_data_dummy
    )
    assert result == ["123"]


@mark.asyncio
@patch.object(AccountCloseStepsService, "_get_user_accounts")
@patch.object(UserPositionsService, "count_positions_by_region")
async def test_verify_positions_when_client_have_positions(
    positions_service_mock, _get_user_accounts_mock
):
    positions_service_mock.return_value = 100
    _get_user_accounts_mock.return_value = ["1", "2", "3"]
    result = await AccountCloseStepsService._verify_positions(
        Region.BR.value, jwt_data_dummy
    )
    assert result is False


@mark.asyncio
@patch.object(AccountCloseStepsService, "_get_user_accounts")
@patch.object(UserPositionsService, "count_positions_by_region")
async def test_verify_positions_when_client_dont_have_positions(
    positions_service_mock, _get_user_accounts_mock
):
    positions_service_mock.return_value = 0
    _get_user_accounts_mock.return_value = ["1", "2", "3"]
    result = await AccountCloseStepsService._verify_positions(
        Region.BR.value, jwt_data_dummy
    )
    assert result is True


@mark.asyncio
@patch.object(EarningsFromClient, "get_service_response")
async def test_verify_earnings_when_client_have_earnings(earnings_service_mock):
    earnigs_result = EarningsRecordResponse(paid=[], payable=[], record_date=[1, 2])
    earnings_service_mock.return_value = earnigs_result
    result = await AccountCloseStepsService._verify_earnings(
        Region.BR.value, jwt_data_dummy
    )
    assert result is False


@mark.asyncio
@patch.object(EarningsFromClient, "get_service_response")
async def test_verify_earnings_when_client_dont_have_earnings(earnings_service_mock):
    earnigs_result = EarningsRecordResponse(paid=[], payable=[], record_date=[])
    earnings_service_mock.return_value = earnigs_result
    result = await AccountCloseStepsService._verify_earnings(
        Region.BR.value, jwt_data_dummy
    )
    assert result is True


@mark.asyncio
@patch.object(AccountCloseStepsService, "_verify_balance")
@patch.object(AccountCloseStepsService, "_verify_positions")
@patch.object(AccountCloseStepsService, "_verify_earnings")
async def test_get_closure_steps_by_region_when_all_true(
    earnings_mock, positions_mock, balance_mock
):
    earnings_mock.return_value = True
    positions_mock.return_value = True
    balance_mock.return_value = True
    result = await AccountCloseStepsService.get_closure_steps_by_region(
        "BR", jwt_data_dummy
    )
    expected_result = (True, {"balance": True, "positions": True, "earnings": True})
    assert result == expected_result


@mark.asyncio
@patch.object(AccountCloseStepsService, "_verify_balance")
@patch.object(AccountCloseStepsService, "_verify_positions")
@patch.object(AccountCloseStepsService, "_verify_earnings")
async def test_get_closure_steps_by_region_when_one_step_is_false(
    earnings_mock, positions_mock, balance_mock
):
    earnings_mock.return_value = False
    positions_mock.return_value = True
    balance_mock.return_value = True
    result = await AccountCloseStepsService.get_closure_steps_by_region(
        "BR", jwt_data_dummy
    )
    expected_result = (False, {"balance": True, "positions": True, "earnings": False})
    assert result == expected_result


@mark.asyncio
async def test_get_service_response_when_region_us_and_all_true(monkeypatch):
    closure_steps_dummy = AccountCloseStepsRequest(region="US")

    async def mock_closure_steps(region, jwt_data):
        if region == "BR":
            result = (True, {"balance": True, "positions": True, "earnings": True})
            return result
        elif region == "US":
            result = (True, {"balance": True, "positions": True, "earnings": True})
            return result

    monkeypatch.setattr(
        AccountCloseStepsService, "get_closure_steps_by_region", mock_closure_steps
    )

    result = await AccountCloseStepsService.get_list_client_orders(
        closure_steps_dummy, jwt_data_dummy
    )
    expected_result = {
        "regular": True,
        "steps_status": {"US": {"balance": True, "positions": True, "earnings": True}},
    }

    assert result == expected_result


@mark.asyncio
async def test_get_service_response_when_region_us_and_one_step_is_false(monkeypatch):
    closure_steps_dummy = AccountCloseStepsRequest(region="US")

    async def mock_closure_steps(region, jwt_data):
        if region == "BR":
            result = (True, {"balance": True, "positions": True, "earnings": True})
            return result
        elif region == "US":
            result = (False, {"balance": False, "positions": True, "earnings": True})
            return result

    monkeypatch.setattr(
        AccountCloseStepsService, "get_closure_steps_by_region", mock_closure_steps
    )

    result = await AccountCloseStepsService.get_list_client_orders(
        closure_steps_dummy, jwt_data_dummy
    )
    expected_result = {
        "regular": False,
        "steps_status": {"US": {"balance": False, "positions": True, "earnings": True}},
    }

    assert result == expected_result


@mark.asyncio
async def test_get_service_response_when_region_br_and_all_true(monkeypatch):
    closure_steps_dummy = AccountCloseStepsRequest(region="BR")

    async def mock_closure_steps(region, jwt_data):
        if region == "BR":
            result = (True, {"balance": True, "positions": True, "earnings": True})
            return result
        elif region == "US":
            result = (True, {"balance": True, "positions": True, "earnings": True})
            return result

    monkeypatch.setattr(
        AccountCloseStepsService, "get_closure_steps_by_region", mock_closure_steps
    )

    result = await AccountCloseStepsService.get_list_client_orders(
        closure_steps_dummy, jwt_data_dummy
    )
    expected_result = {
        "regular": True,
        "steps_status": {
            "BR": {"balance": True, "positions": True, "earnings": True},
            "US": {"balance": True, "positions": True, "earnings": True},
        },
    }

    assert result == expected_result


@mark.asyncio
async def test_get_service_response_when_region_br_and_one_step_is_false(monkeypatch):
    closure_steps_dummy = AccountCloseStepsRequest(region="BR")

    async def mock_closure_steps(region, jwt_data):
        if region == "BR":
            result = (False, {"balance": False, "positions": True, "earnings": True})
            return result
        elif region == "US":
            result = (True, {"balance": True, "positions": True, "earnings": True})
            return result

    monkeypatch.setattr(
        AccountCloseStepsService, "get_closure_steps_by_region", mock_closure_steps
    )

    result = await AccountCloseStepsService.get_list_client_orders(
        closure_steps_dummy, jwt_data_dummy
    )
    expected_result = {
        "regular": False,
        "steps_status": {
            "BR": {"balance": False, "positions": True, "earnings": True},
            "US": {"balance": True, "positions": True, "earnings": True},
        },
    }

    assert result == expected_result


@mark.asyncio
async def test_get_service_response_when_region_br_and_one_step_is_false_in_us(
    monkeypatch,
):
    closure_steps_dummy = AccountCloseStepsRequest(region="BR")

    async def mock_closure_steps(region, jwt_data):
        if region == "BR":
            result = (True, {"balance": True, "positions": True, "earnings": True})
            return result
        elif region == "US":
            result = (False, {"balance": False, "positions": True, "earnings": True})
            return result

    monkeypatch.setattr(
        AccountCloseStepsService, "get_closure_steps_by_region", mock_closure_steps
    )

    result = await AccountCloseStepsService.get_list_client_orders(
        closure_steps_dummy, jwt_data_dummy
    )
    expected_result = {
        "regular": False,
        "steps_status": {
            "BR": {"balance": True, "positions": True, "earnings": True},
            "US": {"balance": False, "positions": True, "earnings": True},
        },
    }

    assert result == expected_result
