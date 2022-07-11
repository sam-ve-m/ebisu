# STANDARD IMPORTS
from unittest.mock import patch
import logging.config

# PROJECT IMPORTS
from decouple import Config, RepositoryEnv

with patch.object(Config, "get", return_value="info"):
    with patch.object(logging.config, "dictConfig"):
        with patch.object(RepositoryEnv, "__init__", return_value=None):
            from src.repositories.earnings.repository import (
                EarningsClientRepository,
                EarningsBrRecord,
            )

# STUB IMPORTS
from tests.src.repositories.earnings.repository_stub import (
    earnings_model_stub,
    earnings_payable_stub,
    earnings_paid_model_stub,
    earnings_paid_stub,
    earnings_record_date_model_stub,
    earnings_record_date_stub,
)


class Iterable:
    def __iter__(self):
        return self


@patch.object(
    EarningsBrRecord, "build_br_earning_model", return_value=earnings_model_stub
)
@patch.object(
    EarningsClientRepository, "get_data", side_effect=[earnings_payable_stub, {}]
)
@patch.object(EarningsBrRecord, "build_earnings_types_where_clause", return_value="")
def test_get_br_payable_earnings_when_sending_right_params_then_return_the_expected(
    mock_get_data, mock_build_earnings_types_where_clause, mock_build_br_earning_model
):
    Iterable.__next__ = mock_get_data
    response = EarningsBrRecord.get_br_payable_earnings(
        account="49", limit=1, earnings_types=None
    )

    assert response == [earnings_model_stub]
    assert isinstance(response, list)


@patch.object(
    EarningsBrRecord, "build_br_earning_model", return_value=earnings_paid_model_stub
)
@patch.object(
    EarningsClientRepository, "get_data", side_effect=[earnings_paid_stub, {}]
)
@patch.object(EarningsBrRecord, "build_earnings_types_where_clause", return_value="")
def test_get_br_paid_earnings_when_sending_right_params_then_return_the_expected(
    mock_get_data, mock_build_earnings_types_where_clause, mock_build_br_earning_model
):
    Iterable.__next__ = mock_get_data
    response = EarningsBrRecord.get_br_paid_earnings(
        account="49", limit=1, earnings_types=None
    )

    assert response == [earnings_paid_model_stub]
    assert isinstance(response, list)


@patch.object(
    EarningsBrRecord,
    "build_br_earning_model",
    return_value=earnings_record_date_model_stub,
)
@patch.object(
    EarningsClientRepository, "get_data", side_effect=[earnings_record_date_stub, {}]
)
@patch.object(EarningsBrRecord, "build_earnings_types_where_clause", return_value="")
def test_get_br_record_date_earnings_when_sending_right_params_then_return_the_expected(
    mock_get_data, mock_build_earnings_types_where_clause, mock_build_br_earning_model
):
    Iterable.__next__ = mock_get_data
    response = EarningsBrRecord.get_br_record_date_earnings(
        account="49", limit=1, earnings_types=None
    )

    assert response == [earnings_record_date_model_stub]
    assert isinstance(response, list)
