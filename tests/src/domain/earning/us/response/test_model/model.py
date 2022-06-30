# STANDARD IMPORTS
from unittest.mock import patch
from datetime import datetime

# PROJECT IMPORTS
from src.domain.earning.us.response.model import EarningsModelToResponse
from src.repositories.earnings.repository import EarningsBrRecord

earnings_transactions_stub = [{'trade_history': 'LC04D00116LIQUIDACAO D', 'trade_type': "NOT INFORMED", 'trade_code': 'PETR4', 'transaction_ammount': -200.0, 'net_price': 5918.0, 'date': "2022-1-14 00:00:00"}]
# 1642699893000
earnings_payable_stub = {'DESC_HIST_MVTO': 'LC04D00116LIQUIDACAO D', 'DESC_RESU_TIPO_MVTO': None, 'COD_NEG': 'PETR4', 'QTDE_MVTO': -200.0, 'PREC_LQDO': 5918.0, 'DATA_MVTO': datetime(2022, 7, 22, 0, 0)}


def test_get_yesterday_date_in_timestamp_then_return_the_expected():
    response = EarningsModelToResponse.get_yesterday_date_in_timestamp()
    assert isinstance(response, int)


def test_earnings_response_when_sending_right_params_then_return_the_expected():
    earning_model = EarningsBrRecord.build_br_earning_model(
        earning_transaction=earnings_payable_stub
    )
    response = EarningsModelToResponse.earnings_response(
        earnings_transactions=[earning_model]
    )
    assert response == ""
