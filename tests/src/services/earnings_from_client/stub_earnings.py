from datetime import datetime

dw_earnings_example = [
            {
                "accountAmount": 1,
                "accountBalance": 1,
                "accountType": "LIVE",
                "comment": "SPHD dividend, $0.1511/share",
                "dividend": {
                    "type": "CASH",
                    "amountPerShare": 0.1511,
                    "taxCode": "FULLY_TAXABLE"
                },
                "dnb": False,
                "finTranID": "GF.b1aa5537-0d7c-4d30-810e-4f0fe4fa6ce4",
                "finTranTypeID": "DIV",
                "feeSec": 0,
                "feeTaf": 0,
                "feeBase": 0,
                "feeXtraShares": 0,
                "feeExchange": 0,
                "fillQty": 0,
                "fillPx": 0,
                "instrument": {
                    "id": "9563a550-9f3b-47aa-b570-f18435f218d2",
                    "symbol": "SPHD",
                    "name": "PowerShares S&P 500 High Div Low Vol ETF"
                },
                "orderID": "0",
                "sendCommissionToInteliclear": False,
                "systemAmount": 0,
                "tranAmount": -2.68,
                "tranSource": "INTE",
                "tranWhen": "2019-06-03T15:12:00.345Z",
                "wlpAmount": 0,
                "wlpFinTranTypeID": "e8ff5103-ad40-4ed9-b2ee-fd96826bf935"
            },
            {
                "accountAmount": 1,
                "accountBalance": 1,
                "accountType": "LIVE",
                "comment": "SPHD dividend, $0.1511/share",
                "dividend": {
                    "type": "CASH",
                    "amountPerShare": 0.1511,
                    "taxCode": "FULLY_TAXABLE"
                },
                "dnb": False,
                "finTranID": "GF.b1aa5537-0d7c-4d30-810e-4f0fe4fa6ce4",
                "finTranTypeID": "DIV",
                "feeSec": 0,
                "feeTaf": 0,
                "feeBase": 0,
                "feeXtraShares": 0,
                "feeExchange": 0,
                "fillQty": 0,
                "fillPx": 0,
                "instrument": {
                    "id": "9563a550-9f3b-47aa-b570-f18435f218d2",
                    "symbol": "SPHD",
                    "name": "PowerShares S&P 500 High Div Low Vol ETF"
                },
                "orderID": "0",
                "sendCommissionToInteliclear": False,
                "systemAmount": 0,
                "tranAmount": -2.68,
                "tranSource": "INTE",
                "tranWhen": "2019-06-03T15:12:00.345Z",
                "wlpAmount": 0,
                "wlpFinTranTypeID": "e8ff5103-ad40-4ed9-b2ee-fd96826bf935"
            },
            {
                "accountAmount": 1,
                "accountBalance": 1,
                "accountType": "LIVE",
                "comment": "SPHD dividend, $0.1511/share",
                "dividend": {
                    "type": "CASH",
                    "amountPerShare": 0.1511,
                    "taxCode": "FULLY_TAXABLE"
                },
                "dnb": False,
                "finTranID": "GF.b1aa5537-0d7c-4d30-810e-4f0fe4fa6ce4",
                "finTranTypeID": "DIV",
                "feeSec": 0,
                "feeTaf": 0,
                "feeBase": 0,
                "feeXtraShares": 0,
                "feeExchange": 0,
                "fillQty": 0,
                "fillPx": 0,
                "instrument": {
                    "id": "9563a550-9f3b-47aa-b570-f18435f218d2",
                    "symbol": "AMD",
                    "name": "PowerShares S&P 500 High Div Low Vol ETF"
                },
                "orderID": "0",
                "sendCommissionToInteliclear": False,
                "systemAmount": 0,
                "tranAmount": -2.68,
                "tranSource": "INTE",
                "tranWhen": "2019-06-03T15:12:00.345Z",
                "wlpAmount": 0,
                "wlpFinTranTypeID": "e8ff5103-ad40-4ed9-b2ee-fd96826bf935"
            },
            {
                "accountAmount": 1,
                "accountBalance": 1,
                "accountType": "LIVE",
                "comment": "SPHD dividend, $0.1511/share",
                "dividend": {
                    "type": "CASH",
                    "amountPerShare": 0.1511,
                    "taxCode": "FULLY_TAXABLE"
                },
                "dnb": False,
                "finTranID": "GF.b1aa5537-0d7c-4d30-810e-4f0fe4fa6ce4",
                "finTranTypeID": "DIV",
                "feeSec": 0,
                "feeTaf": 0,
                "feeBase": 0,
                "feeXtraShares": 0,
                "feeExchange": 0,
                "fillQty": 0,
                "fillPx": 0,
                "instrument": {
                    "id": "9563a550-9f3b-47aa-b570-f18435f218d2",
                    "symbol": "AMD",
                    "name": "PowerShares S&P 500 High Div Low Vol ETF"
                },
                "orderID": "0",
                "sendCommissionToInteliclear": False,
                "systemAmount": 0,
                "tranAmount": -2.68,
                "tranSource": "INTE",
                "tranWhen": "2019-06-03T15:12:00.345Z",
                "wlpAmount": 0,
                "wlpFinTranTypeID": "e8ff5103-ad40-4ed9-b2ee-fd96826bf935"
            },
            {
                "accountAmount": 1,
                "accountBalance": 1,
                "accountType": "LIVE",
                "comment": "SPHD dividend, $0.1511/share",
                "dividend": {
                    "type": "CASH",
                    "amountPerShare": 0.1511,
                    "taxCode": "FULLY_TAXABLE"
                },
                "dnb": False,
                "finTranID": "GF.b1aa5537-0d7c-4d30-810e-4f0fe4fa6ce4",
                "finTranTypeID": "DIV",
                "feeSec": 0,
                "feeTaf": 0,
                "feeBase": 0,
                "feeXtraShares": 0,
                "feeExchange": 0,
                "fillQty": 0,
                "fillPx": 0,
                "instrument": {
                    "id": "9563a550-9f3b-47aa-b570-f18435f218d2",
                    "symbol": "AAPL",
                    "name": "PowerShares S&P 500 High Div Low Vol ETF"
                },
                "orderID": "0",
                "sendCommissionToInteliclear": False,
                "systemAmount": 0,
                "tranAmount": -2.68,
                "tranSource": "INTE",
                "tranWhen": "2019-06-03T15:12:00.345Z",
                "wlpAmount": 0,
                "wlpFinTranTypeID": "e8ff5103-ad40-4ed9-b2ee-fd96826bf935"
            },
            {
                "accountAmount": 1,
                "accountBalance": 1,
                "accountType": "LIVE",
                "comment": "SPHD dividend, $0.1511/share",
                "dividend": {
                    "type": "CASH",
                    "amountPerShare": 0.1511,
                    "taxCode": "FULLY_TAXABLE"
                },
                "dnb": False,
                "finTranID": "GF.b1aa5537-0d7c-4d30-810e-4f0fe4fa6ce4",
                "finTranTypeID": "DIV",
                "feeSec": 0,
                "feeTaf": 0,
                "feeBase": 0,
                "feeXtraShares": 0,
                "feeExchange": 0,
                "fillQty": 0,
                "fillPx": 0,
                "instrument": {
                    "id": "9563a550-9f3b-47aa-b570-f18435f218d2",
                    "symbol": "NVIDIA",
                    "name": "PowerShares S&P 500 High Div Low Vol ETF"
                },
                "orderID": "0",
                "sendCommissionToInteliclear": False,
                "systemAmount": 0,
                "tranAmount": -2.68,
                "tranSource": "INTE",
                "tranWhen": "2019-06-03T15:12:00.345Z",
                "wlpAmount": 0,
                "wlpFinTranTypeID": "e8ff5103-ad40-4ed9-b2ee-fd96826bf935"
            },
            {
                "accountAmount": 1,
                "accountBalance": 1,
                "accountType": "LIVE",
                "comment": "SPHD dividend, $0.1511/share",
                "dividend": {
                    "type": "CASH",
                    "amountPerShare": 0.1511,
                    "taxCode": "FULLY_TAXABLE"
                },
                "dnb": False,
                "finTranID": "GF.b1aa5537-0d7c-4d30-810e-4f0fe4fa6ce4",
                "finTranTypeID": "DIV",
                "feeSec": 0,
                "feeTaf": 0,
                "feeBase": 0,
                "feeXtraShares": 0,
                "feeExchange": 0,
                "fillQty": 0,
                "fillPx": 0,
                "instrument": {
                    "id": "9563a550-9f3b-47aa-b570-f18435f218d2",
                    "symbol": "AAPL",
                    "name": "PowerShares S&P 500 High Div Low Vol ETF"
                },
                "orderID": "0",
                "sendCommissionToInteliclear": False,
                "systemAmount": 0,
                "tranAmount": -2.68,
                "tranSource": "INTE",
                "tranWhen": "2019-06-03T15:12:00.345Z",
                "wlpAmount": 0,
                "wlpFinTranTypeID": "e8ff5103-ad40-4ed9-b2ee-fd96826bf935"
            },
{
                "accountAmount": 1,
                "accountBalance": 1,
                "accountType": "LIVE",
                "comment": "SPHD dividend, $0.1511/share",
                "dividend": {
                    "type": "CASH",
                    "amountPerShare": 5.50,
                    "taxCode": "FULLY_TAXABLE"
                },
                "dnb": False,
                "finTranID": "GF.b1aa5537-0d7c-4d30-810e-4f0fe4fa6ce4",
                "finTranTypeID": "DIV",
                "feeSec": 0,
                "feeTaf": 0,
                "feeBase": 0,
                "feeXtraShares": 0,
                "feeExchange": 0,
                "fillQty": 0,
                "fillPx": 0,
                "instrument": {
                    "id": "9563a550-9f3b-47aa-b570-f18435f218d2",
                    "symbol": "VALE3",
                    "name": "PowerShares S&P 500 High Div Low Vol ETF"
                },
                "orderID": "0",
                "sendCommissionToInteliclear": False,
                "systemAmount": 0,
                "tranAmount": -2.68,
                "tranSource": "INTE",
                "tranWhen": "2019-06-03T15:12:00.345Z",
                "wlpAmount": 0,
                "wlpFinTranTypeID": "e8ff5103-ad40-4ed9-b2ee-fd96826bf935"
            },
{
                "accountAmount": 1,
                "accountBalance": 1,
                "accountType": "LIVE",
                "comment": "SPHD dividend, $0.1511/share",
                "dividend": {
                    "type": "CASH",
                    "amountPerShare": 5.50,
                    "taxCode": "FULLY_TAXABLE"
                },
                "dnb": False,
                "finTranID": "GF.b1aa5537-0d7c-4d30-810e-4f0fe4fa6ce4",
                "finTranTypeID": "DIV",
                "feeSec": 0,
                "feeTaf": 0,
                "feeBase": 0,
                "feeXtraShares": 0,
                "feeExchange": 0,
                "fillQty": 0,
                "fillPx": 0,
                "instrument": {
                    "id": "9563a550-9f3b-47aa-b570-f18435f218d2",
                    "symbol": "PETR4",
                    "name": "PowerShares S&P 500 High Div Low Vol ETF"
                },
                "orderID": "0",
                "sendCommissionToInteliclear": False,
                "systemAmount": 0,
                "tranAmount": -2.68,
                "tranSource": "INTE",
                "tranWhen": "2022-07-03T15:12:00.345Z",
                "wlpAmount": 0,
                "wlpFinTranTypeID": "e8ff5103-ad40-4ed9-b2ee-fd96826bf935"
            },
{
                "accountAmount": 1,
                "accountBalance": 1,
                "accountType": "LIVE",
                "comment": "SPHD dividend, $0.1511/share",
                "dividend": {
                    "type": "CASH",
                    "amountPerShare": 5.50,
                    "taxCode": "FULLY_TAXABLE"
                },
                "dnb": False,
                "finTranID": "GF.b1aa5537-0d7c-4d30-810e-4f0fe4fa6ce4",
                "finTranTypeID": "DIV",
                "feeSec": 0,
                "feeTaf": 0,
                "feeBase": 0,
                "feeXtraShares": 0,
                "feeExchange": 0,
                "fillQty": 0,
                "fillPx": 0,
                "instrument": {
                    "id": "9563a550-9f3b-47aa-b570-f18435f218d2",
                    "symbol": "APPL3",
                    "name": "PowerShares S&P 500 High Div Low Vol ETF"
                },
                "orderID": "0",
                "sendCommissionToInteliclear": False,
                "systemAmount": 0,
                "tranAmount": -2.68,
                "tranSource": "INTE",
                "tranWhen": "2022-10-04T15:12:00.345Z",
                "wlpAmount": 0,
                "wlpFinTranTypeID": "e8ff5103-ad40-4ed9-b2ee-fd96826bf935"
            }
        ]

get_br_payable_earnings_stub = {'description': 'LC04D00116LIQUIDACAO D',
                       'symbol': 'PETR4',
                       'share_quantity': -200.0,
                       'amount_per_share': 5918.0,
                       'date': "2022-7-22 00:00:00"}

get_br_paid_earnings_stub = {'DESC_HIST_MVTO': 'LC04D00116LIQUIDACAO D',
                          'COD_NEG': 'PETR4',
                          'QTDE_MVTO': -200.0,
                          'AMOUNT_PER_SHARE': 5918.0,
                          'DATA_MVTO': datetime(2022, 5, 20, 0, 0)}

get_br_record_date_earnings_stub = {'DESC_HIST_MVTO': 'LC04D00116LIQUIDACAO D',
                          'COD_NEG': 'PETR4',
                          'QTDE_MVTO': -200.0,
                          'AMOUNT_PER_SHARE': 5918.0,
                          'DATA_MVTO': datetime(9999, 12, 31, 0, 0)}

stub_get_service_response = {
    "paid": [{'description': 'LC04D00116LIQUIDACAO D',
            'symbol': 'PETR4',
            'share_quantity': -200.0,
            'net_price': 5918.0,
            'date': "2022-1-14 00:00:00"}],
    "payable": [{'description': 'LC04D00116LIQUIDACAO D',
               'symbol': 'PETR4',
               'share_quantity': -200.0,
               'amount_per_share': 5918.0,
               'date': "2022-7-22 00:00:00"}],
    "record_date": [{'description': 'LC04D00220LIQUIDACAO D',
               'symbol': 'APPL3',
               'share_quantity': -400.0,
               'amount_per_share': 5918.0,
               'date': "9999-12-31 00:00:00"}]
}


get_earnings_response_stub = [{
    "trade_history": "LC03C00006TRANSFERENCIA CRÉDITO",
    "trade_type": None,
    "trade_code": "ALPA4",
    "transaction_amount": 300.0,
    "net_price": 0.0,
    "transaction_date": "2022-07-10"},    {
        "trade_history": "LC03C00006TRANSFERENCIA CRÉDITO",
        "trade_type": None,
        "trade_code": "ALPA4",
        "transaction_amount": 300.0,
        "net_price": 0.0,
        "transaction_date": "2022-05-10"},{
    "trade_history": "LC03C00006TRANSFERENCIA CRÉDITO",
    "trade_type": None,
    "trade_code": "ALPA4",
    "transaction_amount": 300.0,
    "net_price": 0.0,
    "transaction_date": "9999-31-12"}]

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