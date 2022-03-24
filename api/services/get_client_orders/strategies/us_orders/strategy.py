from api.infrastructures.application_dependencies.singletons.oracle import OracleSingletonInstance


class GetUsOrdersDetails:

    oracle_singleton_instance = OracleSingletonInstance.get_oracle_us_singleton_instance()

    @staticmethod
    def build_query(bovespa_account: str, bmf_account: str, clordid: str) -> str:
        query = f"""
                    SELECT C.MESSAGE, A.*
                    FROM UDRIVDB001.VW_HIERARCHY_EXECUTION_REPORTS A
                    LEFT JOIN UORDEDB001.MAP_ORDERS_REJECT_REASON_TO_SIGAME_MESSAGES B ON A.ORDREJREASON = B.B3_MESSAGE_ID
                    LEFT JOIN UORDEDB001.SIGAME_ORDERS_MESSAGES C ON B.SIGAME_MESSAGE_ID = C.SIGAME_MESSAGE_ID
                    WHERE ACCOUNT in ('{bovespa_account}', '{bmf_account}') AND NEWEST_CLORDID = '{clordid}'
                    ORDER BY TRANSACTTIME DESC
                    """
        return query
