from datetime import datetime


earnings_dummy_br = {
    "symbol": "PETR4",
    "timestamp": 1617035799000,
    "offset": 0,
    "limit": "10",
}


normalize_earnings_dummy_request = {
    "SYMBOL": "PETR4",
    "EARNINGS_DATE": datetime(2022, 2, 24, 16, 10, 29, 669000),
    "PRICE": 299,
    "EARNINGS_TYPE": "DIVIDEND",
    "TO_DATE('1970-01-19','YYYY-MM-DD')": datetime(1970, 1, 19, 0, 0),
}

earnings_dummy_response = [
    {
        "symbol": "PETR4",
        "date": "2022-02-24T16:10:29.669000",
        "price": 299,
        "earnings_type": "DIVIDEND",
    }
]

query_dummy_earnings = f"""
                SELECT SYMBOL, EARNINGS_DATE, PRICE, EARNINGS_TYPE, TO_DATE('1617035799000', 'yyyy-mm-dd')
                FROM UDATAEDB001.EARNINGS
                WHERE SYMBOL = UPPER('PETR4')                               
                ORDER BY EARNINGS_DATE DESC
                OFFSET '0' ROWS FETCH NEXT '10' ROWS ONLY
                """
