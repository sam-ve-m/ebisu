import datetime


user_trade_dummy = {'SYMBOL': 'MYPK3',
                    'ORDSTATUS': 'NEW',
                    'CLORDID': '17e05bfa-7df5-434c-baf6-55aebbdf5a7e',
                    'TRANSACTTIME': datetime.datetime(2022, 4, 22, 16, 11, 30, 498000),
                    'CUMQTY': 0,
                    'AVGPX': 0,
                    'ORDTYPE': 'LIMIT',
                    'ORDERQTY': 5000}


normalized_data_dummy = {'name': 'Iochpe Maxion SA',
                         'cl_order_id': '17e05bfa-7df5-434c-baf6-55aebbdf5a7e',
                         'time': 1650654690.498,
                         'quantity': 5000,
                         'order_type': 'LIMIT',
                         'average_price': 0,
                         'currency': 'BRL',
                         'symbol': 'MYPK3',
                         'status': 'NEW',
                         'total_spent': 0.0}


stub_expected_response = [{'average_price': 1.0,
  'cl_order_id': 'f63d5adc9f4b1380c8a3882a80aeb41167cc5835',
  'currency': 'BRL',
  'name': 'CannaPharmaRx Inc',
  'order_type': 'MARKET',
  'quantity': 100,
  'status': 'FILLED',
  'symbol': None,
  'time': 1649791917.348,
  'total_spent': 100.0}]



query_dummy_orders = "SELECT B.SYMBOL, ORDSTATUS, B.CLORDID, B.TRANSACTTIME, B.CUMQTY, B.AVGPX, " \
              "B.ORDTYPE, B.ORDERQTY FROM USOLUDB001.VW_CURRENT_EXECUTION_REPORTS B WHERE " \
              "B.ACCOUNT in ('000000014-6', '14') AND B.ORDSTATUS = 'NEW' ORDER " \
              "BY B.TRANSACTTIME DESC offset 0 rows fetch first 1 row only"


query_dummy_two_status = "SELECT B.SYMBOL, ORDSTATUS, B.CLORDID, B.TRANSACTTIME, B.CUMQTY, " \
                         "B.AVGPX, B.ORDTYPE, B.ORDERQTY, FROM USOLUDB001.VW_CURRENT_EXECUTION_REPORTS " \
                         "B WHERE B.ACCOUNT in ('000000014-6', '14') AND B.ORDSTATUS in ('FILLED', 'NEW') " \
                         "ORDER BY B.TRANSACTTIME DESC offset 0 rows fetch first 1 row only "


open_orders_dummy = [{'SYMBOL': None,
                      'ORDSTATUS': 'FILLED',
                      'CLORDID': 'f63d5adc9f4b1380c8a3882a80aeb41167cc5835',
                      'TRANSACTTIME': datetime.datetime(2022, 4, 12, 16, 31, 57, 348000),
                      'CUMQTY': 100,
                      'AVGPX': 1,
                      'ORDTYPE': 'MARKET',
                      'ORDERQTY': 100}]


open_orders_two_dummy = [{'SYMBOL': 'MYPK3', 'ORDSTATUS': 'FILLED',
                          'CLORDID': 'f63d5adc9f4b1380c8a3882a80aeb41167cc5835',
                          'TRANSACTTIME': datetime.datetime(2022, 4, 12, 16, 31, 57, 348000),
                          'CUMQTY': 100, 'AVGPX': 1, 'ORDTYPE': 'MARKET', 'ORDERQTY': 100},
                         {'SYMBOL': 'PETR4', 'ORDSTATUS': 'FILLED',
                          'CLORDID': 'd325fd1ab4b1593983bcfb95ae0eca483bd4be44',
                          'TRANSACTTIME': datetime.datetime(2022, 4, 12, 16, 27, 34, 832000),
                          'CUMQTY': 100, 'AVGPX': 50, 'ORDTYPE': 'MARKET', 'ORDERQTY': 100}]

client_response = [{  'average_price': 1.0,
                      'cl_order_id': 'f63d5adc9f4b1380c8a3882a80aeb41167cc5835',
                      'currency': 'BRL',
                      'name': 'CannaPharmaRx Inc',
                      'order_type': 'MARKET',
                      'quantity': 100,
                      'status': 'FILLED',
                      'symbol': None,
                      'time': 1649791917.348,
                      'total_spent': 100.0}]


client_two_response = [
    {
        "name": "Iochpe Maxion SA",
        "cl_order_id": "f63d5adc9f4b1380c8a3882a80aeb41167cc5835",
        "time": 1649791917.348,
        "quantity": 100,
        "order_type": "MARKET",
        "average_price": 1.0,
        "currency": "BRL",
        "symbol": "MYPK3",
        "status": "FILLED",
        "total_spent": 100.0
    },
    {
        "name": "Petroleo Brasileiro SA Petrobras",
        "cl_order_id": "d325fd1ab4b1593983bcfb95ae0eca483bd4be44",
        "time": 1649791654.832,
        "quantity": 100,
        "order_type": "MARKET",
        "average_price": 50.0,
        "currency": "BRL",
        "symbol": "PETR4",
        "status": "FILLED",
        "total_spent": 5000.0
    }
]
