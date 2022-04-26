statement_dummy_request = {'region': 'BR',
                           'limit': 4,
                           'offset': 20,
                           'start_date': 1646757399000,
                           'end_date': 1648485399000}

statement_another_dummy_request = {'region': 'LR',
                                   'limit': 4,
                                   'offset': 20,
                                   'start_date': 0,
                                   'end_date': 0}

dummy_statement_response_br = {
    "balance": 987654.3,
    "statements": [{
        "date": 123456.7,
        "description": "Comprovante de Bolsa para 09/03/2022 NC: 827   ",
        "value": -23456.98
    }]}

dummy_statement_response_us = {
    "balance": 8765432.22,
    "statements": [{
            "date": 1646794800.0,
            "description": "Comprovante de Bolsa para 09/03/2022 NC: 827   ",
            "value": 5234.00
        }]}

query_dummy = f"""SELECT DT_LANCAMENTO, DS_LANCAMENTO, VL_LANCAMENTO 
                   FROM xxxx.xxxx
                   WHERE CD_CLIENTE = '20'
                   AND DT_LANCAMENTO >= TO_DATE('1646757399000', 'yyyy-MM-dd')
                   AND DT_LANCAMENTO <= TO_DATE('1648485399000', 'yyyy-MM-dd')                   
                   ORDER BY NR_LANCAMENTO
                   OFFSET 1 rows
                   fetch first 2 row only
                   """

