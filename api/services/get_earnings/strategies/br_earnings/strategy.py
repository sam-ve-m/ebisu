from api.infrastructures.application_dependencies.singletons.oracle import OracleSingletonInstance


class GetBrEarnings:
    oracle_earnings_singleton_instance = OracleSingletonInstance.get_earnings_singleton_instance()

    @staticmethod
    def build_query_earnings(symbol: str, timestamp: str, limit: int, offset: int) -> str:
        query = f"""
                SELECT SYMBOL, EARNINGS_DATE, PRICE, EARNINGS_TYPE, TO_DATE('{timestamp}', 'yyyy-mm-dd')
                FROM UDATAEDB001.EARNINGS
                WHERE SYMBOL = UPPER('{symbol}')                               
                ORDER BY EARNINGS_DATE DESC
                OFFSET {offset} ROWS FETCH NEXT {limit} ROWS ONLY
                """
        return query
