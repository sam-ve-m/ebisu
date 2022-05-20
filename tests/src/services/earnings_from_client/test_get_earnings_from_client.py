# STANDARD LIBS
import pytest
from unittest.mock import patch, MagicMock

# external imports
from pydantic import ValidationError

from src.exceptions.exceptions import UnauthorizedError
from src.services.earnings_from_client.get_earnings_from_client import (
    EarningsFromClient,
)
from src.domain.validators.exchange_info.get_earnings_client import EarningsClientModel
from tests.src.stubs.project_stubs.stub_data import payload_data_dummy
from src.services.earnings_from_client.strategies.br import GetBrEarningsDetails
from src.repositories.base_repositories.oracle.repository import OracleBaseRepository

# stubs
from tests.src.stubs.router_exchange_infos.stubs import scope_stub

earnings_response_stub = {
    "payable_earnings": [
        {
            "client_code": 111,
            "trade_history": "LC03C00006TRANSFERENCIA CRÃ‰DITO",
            "trade_type": None,
            "trade_code": "ALPA4",
            "transaction_amount": 300.0,
            "net_price": 0.0,
            "transaction_date": "2022-05-02T00:00:00",
        }
    ],
    "record_date_earnings": [
        {
            "client_code": 111,
            "trade_history": "LC03D00005TRANSFERENCIA DÃ‰BITO",
            "trade_type": None,
            "trade_code": "ALPA4",
            "transaction_amount": -300.0,
            "net_price": 0.0,
            "transaction_date": "9999-12-31T00:00:00",
        }
    ],
}

earnings_client_response_stub = {
    "payable_earnings": [
        {
            "client_code": 111,
            "net_price": 0.0,
            "trade_code": "ALPA4",
            "trade_history": "LC03C00006TRANSFERENCIA CRÉDITO",
            "trade_type": None,
            "transaction_amount": 300.0,
            "transaction_date": "2022-05-10",
        }
    ],
    "record_date_earnings": [],
}

client_earnings_stub = [
    {
        "COD_CLI": 111,
        "DESC_HIST_MVTO": "LC03C00006TRANSFERENCIA CRÉDITO",
        "DESC_RESU_TIPO_MVTO": "TRANSFERENCIA",
        "COD_NEG": "ALPA4",
        "QTDE_MVTO": 300.0,
        "PREC_LQDO": 0.0,
        "DATA_MVTO": "2022-05-10",
    }
]
client_earnings_2_stub = {}
normalize_param_stub = {
    "COD_CLI": 111,
    "DESC_HIST_MVTO": "LC03C00006TRANSFERENCIA CRÉDITO",
    "DESC_RESU_TIPO_MVTO": "TRANSFERENCIA",
    "COD_NEG": "ALPA4",
    "QTDE_MVTO": 300.0,
    "PREC_LQDO": 0.0,
    "DATA_MVTO": "2022-05-10",
}
normalized_stub = {
    "client_code": 111,
    "trade_history": "LC03C00006TRANSFERENCIA CRÉDITO",
    "trade_type": None,
    "trade_code": "ALPA4",
    "transaction_amount": 300.0,
    "net_price": 0.0,
    "transaction_date": "2022-05-10",
}


def test_when_sending_the_right_params_then_return_the_normalized_data():
    response = EarningsFromClient.normalize_earnings_data(
        client_earnings=normalize_param_stub
    )
    assert response == normalized_stub
    assert isinstance(response, dict)
    assert response.get("client_code") == 111


def test_when_sending_the_right_params_to_get_account_by_region_then_return_the_expected():
    response = EarningsFromClient.get_account_by_region(
        portfolios={"bovespa_account": "000000014-6", "bmf_account": "14"}, region="BR"
    )
    assert response == "14"
    assert isinstance(response, str)


class Iterable:
    def __iter__(self):
        return self


@patch(
    "src.services.earnings_from_client.get_earnings_from_client.earnings_client_region"
)
@patch.object(
    GetBrEarningsDetails, "build_query_payable_earnings", return_value=MagicMock
)
@patch.object(
    GetBrEarningsDetails, "build_query_record_date_earnings", return_value=MagicMock
)
@patch.object(OracleBaseRepository, "get_data", side_effect=[client_earnings_stub, {}])
def test_when_sending_the_right_params_to_earnings_client_get_response_then_return_the_expected(
    mock_get_data,
    mock_build_query_record_date_earnings,
    mock_build_query_payable_earnings,
    mock_earnings_region,
):
    mock_earnings_region.__getitem__ = MagicMock(return_value=GetBrEarningsDetails)

    Iterable.__next__ = mock_get_data

    response = EarningsFromClient.get_service_response(
        earnings_client=EarningsClientModel(
            **{"region": "BR", "limit": 2, "offset": 0}
        ),
        jwt_data=payload_data_dummy,
    )

    assert response == earnings_client_response_stub


def test_earnings_from_client_response_when_the_params_are_not_valid_then_raise_error_as_expected():
    with pytest.raises(ValidationError):
        EarningsFromClient.get_service_response(
            earnings_client=EarningsClientModel(
                **{"region": None, "limit": None, "offset": None}
            ),
            jwt_data=payload_data_dummy,
        )


def test_earnings_from_client_response_when_the_jwt_is_not_valid_then_raise_error_as_expected():
    with pytest.raises(AttributeError):
        EarningsFromClient.get_service_response(
            earnings_client=EarningsClientModel(
                **{"region": "BR", "limit": 2, "offset": 0}
            ),
            jwt_data=None,
        )
