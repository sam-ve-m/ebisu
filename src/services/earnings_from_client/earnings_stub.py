get_br_payable_earnings_stub = {
    "DESC_HIST_MVTO": "LC03C00006TRANSFERENCIA CRÉDITO",
    "DESC_RESU_TIPO_MVTO": "TRANSFERENCIA",
    "COD_NEG": "ALPA4",
    "QTDE_MVTO": 300.0,
    "PREC_LQDO": 0.0,
    "DATA_MVTO": "2022-07-10",
}

get_br_paid_earnings_stub = {
    "DESC_HIST_MVTO": "LC03C00006TRANSFERENCIA CRÉDITO",
    "DESC_RESU_TIPO_MVTO": "TRANSFERENCIA",
    "COD_NEG": "ALPA4",
    "QTDE_MVTO": 300.0,
    "PREC_LQDO": 0.0,
    "DATA_MVTO": "2022-05-10",
}

get_br_record_date_earnings_stub = {
    "DESC_HIST_MVTO": "LC03C00006TRANSFERENCIA CRÉDITO",
    "DESC_RESU_TIPO_MVTO": "TRANSFERENCIA",
    "COD_NEG": "ALPA4",
    "QTDE_MVTO": 300.0,
    "PREC_LQDO": 0.0,
    "DATA_MVTO": "9999-31-12",
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