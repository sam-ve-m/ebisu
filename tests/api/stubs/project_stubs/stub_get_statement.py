import datetime
from unittest.mock import MagicMock

statement_valid_params = MagicMock(region=MagicMock(value='BR'),limit=1, offset=1, start_date=1646757399000,end_date=1648485399000)
statement_params = MagicMock(region=MagicMock(value='ZR'),limit=1,offset=1,start_date=0,end_date=0)
statement_valid_params_us = MagicMock(region=MagicMock(value='US'),limit=1, offset=1, start_date=1646757399000,end_date=1648485399000)
statement_invalid_params_us = MagicMock(region=MagicMock(value='ZR'),limit=1, offset=1, start_date=0,end_date=0)

dummy_bank_statement_response = {
    "balance": 10000.2,
    "statements": []
}


query_dummy = f"""SELECT DT_LANCAMENTO, DS_LANCAMENTO, VL_LANCAMENTO 
                   FROM xxxx.xxxx
                   WHERE CD_CLIENTE = '20'
                   AND DT_LANCAMENTO >= TO_DATE('1646757399000', 'yyyy-MM-dd')
                   AND DT_LANCAMENTO <= TO_DATE('1648485399000', 'yyyy-MM-dd')                   
                   ORDER BY NR_LANCAMENTO
                   OFFSET 1 rows
                   fetch first 2 row only
                   """
