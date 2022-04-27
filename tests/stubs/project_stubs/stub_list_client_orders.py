import datetime

single_client_orders_response = [{
    "name": "Banco da Lala SA",
    "cl_order_id": "91819229-7d8e-4ea4-b62b-8c9ccc1440b4",
    "time": 1649800978.0,
    "quantity": 100,
    "order_type": "LIMIT",
    "average_price": 50.19,
    "currency": "BRL",
    "symbol": "LALA3",
    "status": "FILLED",
    "total_spent": 5019.0
}]

list_client_orders_response = [
    {
        "name": "Iochpe Maxion SA",
        "cl_order_id": "17e05bfa-7df5-434c-baf6-55aebbdf5a7e",
        "time": 1650654690.0,
        "quantity": 5000,
        "order_type": "LIMIT",
        "average_price": 0,
        "currency": "BRL",
        "symbol": "MYPK3",
        "status": "NEW",
        "total_spent": 0.0
    },
    {
        "name": "Banco da Amazonia SA",
        "cl_order_id": "91819229-7d8e-4ea4-b62b-8c9ccc1440b4",
        "time": 1649800978.0,
        "quantity": 100,
        "order_type": "LIMIT",
        "average_price": 50.19,
        "currency": "BRL",
        "symbol": "BAZA3",
        "status": "FILLED",
        "total_spent": 5019.0
    }
]

user_trade_dummy = {'SYMBOL': 'LELE3',
                    'ORDSTATUS': 'NEW',
                    'CLORDID': '17e05bfa-7df5-434c-baf6-55aebbdf5a7e',
                    'TRANSACTTIME': datetime.datetime(2022, 4, 22, 16, 11, 30, 498000),
                    'CUMQTY': 0,
                    'AVGPX': 0,
                    'ORDTYPE': 'LIMIT',
                    'ORDERQTY': 5000}

field_dummy = 'AVGPX'

normalized_data_dummy = {'name': 'LELE3',
                         'cl_order_id': '17e05bfa-7df5-434c-baf6-55aebbdf5a7e',
                         'time': 1650654690.0,
                         'quantity': 5000,
                         'order_type': 'LIMIT',
                         'average_price': 0,
                         'currency': 'BRL',
                         'symbol': 'MYPK3',
                         'status': 'NEW',
                         'total_spent': 0.0}
