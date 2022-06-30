# STANDARD IMPORTS
from unittest.mock import patch
import pytest
from datetime import datetime

# PROJECT IMPORTS
from src.repositories.earnings.repository import EarningsClientRepository, EarningsBrRecord


earnings_payable_stub = [{'DESC_HIST_MVTO': 'LC04D00116LIQUIDACAO D', 'DESC_RESU_TIPO_MVTO': None, 'COD_NEG': 'PETR4', 'QTDE_MVTO': -200.0, 'PREC_LQDO': 5918.0, 'DATA_MVTO': datetime(2022, 7, 22, 0, 0)}]
earnings_model_stub = [{'trade_history': 'LC04D00116LIQUIDACAO D', 'trade_type': "NOT INFORMED", 'trade_code': 'PETR4', 'transaction_ammount': -200.0, 'net_price': 5918.0, 'date': datetime(2022, 7, 22, 0, 0)}]


class Iterable:
    def __iter__(self):
        return self


@patch.object(EarningsClientRepository, "get_data", side_effect=[earnings_payable_stub, {}])
@patch.object(EarningsBrRecord, "build_earnings_types_where_clause", return_value="")
def test_get_br_payable_earnings_when_sending_right_params_then_return_the_expected(
        mock_get_data, mock_build_earnings_types_where_clause
):
    Iterable.__next__ = mock_get_data
    response = EarningsBrRecord.get_br_payable_earnings(
        account="49",
        limit=1,
        offset=0,
        earnings_types=None
    )

    assert response == earnings_model_stub
