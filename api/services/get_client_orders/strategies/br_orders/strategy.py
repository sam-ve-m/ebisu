from typing import List

from api.domain.enums.order_status import OrderStatus


class GetBrOrdersDetails:
    oracle_singleton_instance = None

    @staticmethod
    def build_query(bovespa_account: str, bmf_account: str, clordid: str) -> str:
        query = f"""SELECT * from USOLUDB001.EXECUTION_REPORTS 
                    WHERE ACCOUNT in ('{bovespa_account}', '{bmf_account}') AND CLORDID = '{clordid}'
                    ORDER BY TRANSACTTIME ASC"""
        return query

