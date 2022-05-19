import datetime


user_trade_dummy = {
    "SYMBOL": "MYPK3",
    "ORDSTATUS": "NEW",
    "CLORDID": "17e05bfa-7df5-434c-baf6-55aebbdf5a7e",
    "TRANSACTTIME": datetime.datetime(2022, 4, 22, 16, 11, 30, 498000),
    "CUMQTY": 0,
    "AVGPX": 0,
    "ORDTYPE": "LIMIT",
    "ORDERQTY": 5000,
}


normalized_data_dummy = {
    "name": "Iochpe Maxion SA",
    "cl_order_id": "17e05bfa-7df5-434c-baf6-55aebbdf5a7e",
    "time": 1650654690.498,
    "quantity": 5000,
    "order_type": "LIMIT",
    "average_price": 0,
    "currency": "BRL",
    "symbol": "MYPK3",
    "status": "NEW",
    "total_spent": 0.0,
}

get_data_stub = [
    {
        "SYMBOL": "JBSS3",
        "ORDSTATUS": "NEW",
        "CLORDID": "af7ed971b0872011b2b2ca86378da3780bfef0ba",
        "TRANSACTTIME": datetime.datetime(2022, 5, 3, 19, 44, 31, 867000),
        "CUMQTY": 0,
        "AVGPX": 0,
        "ORDTYPE": "STOP_LOSS",
        "ORDERQTY": 100,
    }
]

get_data_two_status_stub = [
    {
        "SYMBOL": "JBSS3",
        "ORDSTATUS": "NEW",
        "CLORDID": "af7ed971b0872011b2b2ca86378da3780bfef0ba",
        "TRANSACTTIME": datetime.datetime(2022, 5, 3, 19, 44, 31, 867000),
        "CUMQTY": 0,
        "AVGPX": 0,
        "ORDTYPE": "STOP_LOSS",
        "ORDERQTY": 100,
    },
    {
        "SYMBOL": "VALE3",
        "ORDSTATUS": "CANCELLED",
        "CLORDID": "93355b54cf51e99e3e7f0695cb37959b272ffc23",
        "TRANSACTTIME": datetime.datetime(2022, 5, 3, 17, 59, 18, 624000),
        "CUMQTY": 0,
        "AVGPX": 0,
        "ORDTYPE": "STOP_LOSS",
        "ORDERQTY": 100,
    },
]

normalized_data_stub = {
    "name": "JBS SA",
    "cl_order_id": "af7ed971b0872011b2b2ca86378da3780bfef0ba",
    "time": 1651617871.867,
    "quantity": 100,
    "order_type": "STOP_LOSS",
    "average_price": 0,
    "currency": "BRL",
    "symbol": "JBSS3",
    "status": "NEW",
    "total_spent": 0.0,
}

normalized_data_second_status = {
    "name": "VALE SA",
    "cl_order_id": "93355b54cf51e99e3e7f0695cb37959b272ffc23",
    "time": 1651611558.624,
    "quantity": 100,
    "order_type": "STOP_LOSS",
    "average_price": 0,
    "currency": "BRL",
    "symbol": "VALE3",
    "status": "CANCELLED",
    "total_spent": 0.0,
}

stub_expected_response = [
    {
        "average_price": 1.0,
        "cl_order_id": "f63d5adc9f4b1380c8a3882a80aeb41167cc5835",
        "currency": "BRL",
        "name": "CannaPharmaRx Inc",
        "order_type": "MARKET",
        "quantity": 100,
        "status": "FILLED",
        "symbol": None,
        "time": 1649791917.348,
        "total_spent": 100.0,
    }
]


query_dummy_orders = (
    "SELECT B.SYMBOL, ORDSTATUS, B.CLORDID, B.TRANSACTTIME, B.CUMQTY, B.AVGPX, "
    "B.ORDTYPE, B.ORDERQTY FROM USOLUDB001.VW_CURRENT_EXECUTION_REPORTS B WHERE "
    "B.ACCOUNT in ('000000014-6', '14') AND B.ORDSTATUS = 'NEW' ORDER "
    "BY B.TRANSACTTIME DESC offset 0 rows fetch first 1 row only"
)


query_dummy_two_status = (
    "SELECT B.SYMBOL, ORDSTATUS, B.CLORDID, B.TRANSACTTIME, B.CUMQTY, "
    "B.AVGPX, B.ORDTYPE, B.ORDERQTY, FROM USOLUDB001.VW_CURRENT_EXECUTION_REPORTS "
    "B WHERE B.ACCOUNT in ('000000014-6', '14') AND B.ORDSTATUS in ('FILLED', 'NEW') "
    "ORDER BY B.TRANSACTTIME DESC offset 0 rows fetch first 1 row only "
)


open_orders_dummy = [
    {
        "SYMBOL": None,
        "ORDSTATUS": "FILLED",
        "CLORDID": "f63d5adc9f4b1380c8a3882a80aeb41167cc5835",
        "TRANSACTTIME": datetime.datetime(2022, 4, 12, 16, 31, 57, 348000),
        "CUMQTY": 100,
        "AVGPX": 1,
        "ORDTYPE": "MARKET",
        "ORDERQTY": 100,
    }
]


open_orders_two_dummy = [
    {
        "SYMBOL": "MYPK3",
        "ORDSTATUS": "FILLED",
        "CLORDID": "f63d5adc9f4b1380c8a3882a80aeb41167cc5835",
        "TRANSACTTIME": datetime.datetime(2022, 4, 12, 16, 31, 57, 348000),
        "CUMQTY": 100,
        "AVGPX": 1,
        "ORDTYPE": "MARKET",
        "ORDERQTY": 100,
    },
    {
        "SYMBOL": "PETR4",
        "ORDSTATUS": "FILLED",
        "CLORDID": "d325fd1ab4b1593983bcfb95ae0eca483bd4be44",
        "TRANSACTTIME": datetime.datetime(2022, 4, 12, 16, 27, 34, 832000),
        "CUMQTY": 100,
        "AVGPX": 50,
        "ORDTYPE": "MARKET",
        "ORDERQTY": 100,
    },
]

client_response = [
    {
        "average_price": 1.0,
        "cl_order_id": "f63d5adc9f4b1380c8a3882a80aeb41167cc5835",
        "currency": "BRL",
        "name": "CannaPharmaRx Inc",
        "order_type": "MARKET",
        "quantity": 100,
        "status": "FILLED",
        "symbol": None,
        "time": 1649791917.348,
        "total_spent": 100.0,
    }
]


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
        "total_spent": 100.0,
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
        "total_spent": 5000.0,
    },
]

data_response_stub = [
    {
        "average_price": 0,
        "cl_order_id": "af7ed971b0872011b2b2ca86378da3780bfef0ba",
        "currency": "BRL",
        "name": "JBS SA",
        "order_type": "STOP_LOSS",
        "quantity": 100,
        "status": "NEW",
        "symbol": "JBSS3",
        "time": 1651617871.867,
        "total_spent": 0.0,
    }
]

data_two_response = [
    {
        "name": "JBS SA",
        "cl_order_id": "af7ed971b0872011b2b2ca86378da3780bfef0ba",
        "time": 1651617871.867,
        "quantity": 100,
        "order_type": "STOP_LOSS",
        "average_price": 0,
        "currency": "BRL",
        "symbol": "JBSS3",
        "status": "NEW",
        "total_spent": 0.0,
    },
    {
        "name": "VALE SA",
        "cl_order_id": "93355b54cf51e99e3e7f0695cb37959b272ffc23",
        "time": 1651611558.624,
        "quantity": 100,
        "order_type": "STOP_LOSS",
        "average_price": 0,
        "currency": "BRL",
        "symbol": "VALE3",
        "status": "CANCELLED",
        "total_spent": 0.0,
    },
]
