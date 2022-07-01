# STANDARD IMPORTS
from datetime import datetime


earnings_payable_stub = [{'DESC_HIST_MVTO': 'LC04D00116LIQUIDACAO D',
                          'COD_NEG': 'PETR4',
                          'QTDE_MVTO': -200.0,
                          'AMOUNT_PER_SHARE': 5918.0,
                          'DATA_MVTO': datetime(2022, 7, 22, 0, 0)}]
earnings_model_stub = {'description': 'LC04D00116LIQUIDACAO D',
                       'symbol': 'PETR4',
                       'share_quantity': -200.0,
                       'amount_per_share': 5918.0,
                       'date': "2022-7-22 00:00:00"}

earnings_paid_stub = [{'DESC_HIST_MVTO': 'LC04D00116LIQUIDACAO D',
                       'COD_NEG': 'VALE3',
                       'QTDE_MVTO': -300.0,
                       'AMOUNT_PER_SHARE': 2020.0,
                       'DATA_MVTO': datetime(2022, 1, 14, 0, 0)}]
earnings_paid_model_stub = {'description': 'LC04D00116LIQUIDACAO D',
                            'symbol': 'PETR4',
                            'share_quantity': -200.0,
                            'net_price': 5918.0,
                            'date': "2022-1-14 00:00:00"}

earnings_record_date_stub = [{'DESC_HIST_MVTO': 'LC04D00220LIQUIDACAO D',
                              'COD_NEG': 'APPL3',
                              'QTDE_MVTO': -400.0,
                              'AMOUNT_PER_SHARE': 3030.0,
                              'DATA_MVTO': datetime(2022, 12, 30, 0, 0)}]
earnings_record_date_model_stub = {'description': 'LC04D00220LIQUIDACAO D',
                                   'symbol': 'APPL3',
                                   'share_quantity': -400.0,
                                   'amount_per_share': 5918.0,
                                   'date': "2022-12-30 00:00:00"}
