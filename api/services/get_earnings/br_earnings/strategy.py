class GetBrEarnings:
    oracle_earnings_singleton_instance = None

    @staticmethod
    # todo - checar se esses parametros são corretos
    def build_query_earnings(symbol: str, timestamp: str, limit: int, offset: int) -> str:
        query = f"""
                SELECT SYMBOL, EARNINGS_DATE, PRICE, EARNINGS_TYPE
                FROM UDATAEDB001.EARNINGS
                WHERE SYMBOL in ('{symbol}')
                ORDER BY "xxxx"
                """
        return query
