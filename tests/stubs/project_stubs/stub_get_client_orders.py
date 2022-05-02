import datetime
from unittest.mock import MagicMock


client_order_response_dummy = [
    {
        "cl_order_id": "008cf873-ee2a-4b08-b277-74b8b17f6e64",
        "account": "000000049-9",
        "time": 1644626388.0,
        "quantity": 100,
        "average_price": 0,
        "price": 0,
        "last_price": 0,
        "stop_price": 0,
        "currency": "BRL",
        "symbol": "VALE3",
        "side": "buy",
        "status": "REJECTED",
        "tif": "DAY",
        "total_spent": 0.0,
        "quantity_filled": 0.0,
        "quantity_leaves": 0,
        "quantity_last": 0,
        "text": "Please Contact Admin/Brokerage for Help -> Sem saldo para esta operacao. "
                " Login: INTEGRALIONX. Vlr.Disp R$: -12.490.989,95. Vlr total da ordem "
                "R$: 9.600,00. Compras em aberto R$: 0,00",
        "reject_reason": 0,
        "exec_type": "REJECTED",
        "expire_date": None,
        "error_message": None
    }
]

dummy_user_trade = {'MESSAGE': None,
                    'ACCOUNT': '000000049-9',
                    'AVGPX': 0,
                    'CLORDID': '008cf873-ee2a-4b08-b277-74b8b17f6e64',
                    'CUMQTY': 0,
                    'EXECID': '202202111839486753055',
                    'EXECTYPE': 'REJECTED',
                    'EXPIREDATE': None,
                    'LASTPX': 0,
                    'LASTQTY': 0,
                    'LEAVESQTY': 0,
                    'ORDERID': '20220211063948675',
                    'ORDERQTY': 100,
                    'ORDREJREASON': 0,
                    'ORDSTATUS': 'REJECTED',
                    'ORIGCLORDID': None,
                    'PRICE': None,
                    'SIDE': 'BUY',
                    'STOPPX': None,
                    'SYMBOL': 'VALE3',
                    'TEXT': 'Please Contact Admin/Brokerage for Help -> Sem saldo para esta operacao. '
                            ' Login: INTEGRALIONX. Vlr.Disp R$: -12.490.989,95. Vlr total da ordem '
                            'R$: 9.600,00. Compras em aberto R$: 0,00',
                    'TIMEINFORCE': 'DAY',
                    'TRANSACTTIME': datetime.datetime(2022, 2, 11, 21, 39, 48, 675000),
                    'ORDTYPE': None,
                    'PORTFOLIOID': None,
                    'WORKINGINDICATOR': None,
                    'SENDINGTIME': None,
                    'CXLREJREASON': None,
                    'CXLREJRESPONSETO': None,
                    'NODE_CLORDID': '008cf873-ee2a-4b08-b277-74b8b17f6e64',
                    'NODE_ACCOUNT': '000000049-9'}

dummy_normalized_data = {'cl_order_id': '008cf873-ee2a-4b08-b277-74b8b17f6e64',
                         'account': '000000049-9',
                         'time': 1644626388.0,
                         'quantity': 100,
                         'average_price': 0,
                         'price': 0,
                         'last_price': 0,
                         'stop_price': 0,
                         'currency': 'BRL',
                         'symbol': 'VALE3',
                         'side': 'buy',
                         'status': 'REJECTED',
                         'tif': 'DAY',
                         'total_spent': 0.0,
                         'quantity_filled': 0.0,
                         'quantity_leaves': 0,
                         'quantity_last': 0,
                         'text': 'Please Contact Admin/Brokerage for Help -> '
                                 'Sem saldo para esta operacao.  Login: INTEGRALIONX. '
                                 'Vlr.Disp R$: -12.490.989,95. Vlr total da ordem '
                                 'R$: 9.600,00. Compras em aberto R$: 0,00',
                         'reject_reason': 0,
                         'exec_type': 'REJECTED',
                         'expire_date': None,
                         'error_message': None}

query_dummy_get_client = """SELECT C.MESSAGE, A.* FROM USOLUDB001.VW_HIERARCHY_EXECUTION_REPORTS A LEFT JOIN UORDEDB001.MAP_ORDERS_REJECT_REASON_TO_SIGAME_MESSAGES B ON A.ORDREJREASON = B.B3_MESSAGE_ID LEFT JOIN UORDEDB001.SIGAME_ORDERS_MESSAGES C ON B.SIGAME_MESSAGE_ID = C.SIGAME_MESSAGE_ID WHERE NODE_ACCOUNT in ('000000049-9', '49') AND NODE_CLORDID = '008cf873-ee2a-4b08-b277-74b8b17f6e64' ORDER BY TRANSACTTIME DESC"""

user_open_orders_dummy = [{'MESSAGE': None,
                           'ACCOUNT': '000000049-9',
                           'AVGPX': 0,
                           'CLORDID': '008cf873-ee2a-4b08-b277-74b8b17f6e64',
                           'CUMQTY': 0,
                           'EXECID': '202202111839486753055',
                           'EXECTYPE': 'REJECTED',
                           'EXPIREDATE': None,
                           'LASTPX': 0,
                           'LASTQTY': 0,
                           'LEAVESQTY': 0,
                           'ORDERID': '20220211063948675',
                           'ORDERQTY': 100,
                           'ORDREJREASON': 0,
                           'ORDSTATUS': 'REJECTED',
                           'ORIGCLORDID': None,
                           'PRICE': None,
                           'SIDE': 'BUY',
                           'STOPPX': None,
                           'SYMBOL': 'VALE3',
                           'TEXT': 'Please Contact Admin/Brokerage for Help -> '
                                   'Sem saldo para esta operacao.  Login: INTEGRALIONX.'
                                   ' Vlr.Disp R$: -12.490.989,95. Vlr total da ordem'
                                   ' R$: 9.600,00. Compras em aberto R$: 0,00',
                           'TIMEINFORCE': 'DAY',
                           'TRANSACTTIME': datetime.datetime(2022, 2, 11, 21, 39, 48, 675000),
                           'ORDTYPE': None,
                           'PORTFOLIOID': None,
                           'WORKINGINDICATOR': None,
                           'SENDINGTIME': None,
                           'CXLREJREASON': None,
                           'CXLREJRESPONSETO': None,
                           'NODE_CLORDID': '008cf873-ee2a-4b08-b277-74b8b17f6e64',
                           'NODE_ACCOUNT': '000000049-9'}]

clorder_invalid_params_us = MagicMock(region=MagicMock(value='ZR'), cl_order_id='008cf873-ee2a-4b08-b277-74b8b17f6e64')
