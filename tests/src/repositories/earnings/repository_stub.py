# STANDARD IMPORTS
from datetime import datetime


earnings_payable_stub = [{'DESC_HIST_MVTO': 'LC04D00116LIQUIDACAO D', 'DESC_RESU_TIPO_MVTO': None, 'COD_NEG': 'PETR4', 'QTDE_MVTO': -200.0, 'PREC_LQDO': 5918.0, 'DATA_MVTO': datetime(2022, 7, 22, 0, 0)}]
earnings_model_stub = {'trade_history': 'LC04D00116LIQUIDACAO D', 'trade_type': "NOT INFORMED", 'trade_code': 'PETR4', 'transaction_ammount': -200.0, 'net_price': 5918.0, 'date': "2022-7-22 00:00:00"}

earnings_paid_stub = [{'DESC_HIST_MVTO': 'LC04D00116LIQUIDACAO D', 'DESC_RESU_TIPO_MVTO': None, 'COD_NEG': 'VALE3', 'QTDE_MVTO': -300.0, 'PREC_LQDO': 2020.0, 'DATA_MVTO': datetime(2022, 1, 14, 0, 0)}]
earnings_paid_model_stub = {'trade_history': 'LC04D00116LIQUIDACAO D', 'trade_type': "NOT INFORMED", 'trade_code': 'PETR4', 'transaction_ammount': -200.0, 'net_price': 5918.0, 'date': "2022-1-14 00:00:00"}

earnings_record_date_stub = [{'DESC_HIST_MVTO': 'LC04D00220LIQUIDACAO D', 'DESC_RESU_TIPO_MVTO': None, 'COD_NEG': 'APPL3', 'QTDE_MVTO': -400.0, 'PREC_LQDO': 3030.0, 'DATA_MVTO': datetime(2022, 12, 30, 0, 0)}]
earnings_record_date_model_stub = {'trade_history': 'LC04D00220LIQUIDACAO D', 'trade_type': "NOT INFORMED", 'trade_code': 'APPL3', 'transaction_ammount': -400.0, 'net_price': 5918.0, 'date': "2022-12-30 00:00:00"}
