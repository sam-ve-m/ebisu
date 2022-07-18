from src.repositories.orders.br.repository import BrOrdersRepository
from typing import List


class GetBrOrdersDetails:

    oracle_singleton_instance = BrOrdersRepository

    @staticmethod
    def build_query(accounts: List[str], clordid: str) -> str:
        query = f"""SELECT C.MESSAGE, A.*
                    FROM USOLUDB001.VW_HIERARCHY_EXECUTION_REPORTS A
                    LEFT JOIN UORDEDB001.MAP_ORDERS_REJECT_REASON_TO_SIGAME_MESSAGES B ON A.ORDREJREASON = B.B3_MESSAGE_ID
                    LEFT JOIN UORDEDB001.SIGAME_ORDERS_MESSAGES C ON B.SIGAME_MESSAGE_ID = C.SIGAME_MESSAGE_ID
                    WHERE NODE_ACCOUNT in ('{"', '".join(accounts)}') AND NODE_CLORDID = '{clordid}'
                    ORDER BY CREATEDAT DESC
                    """
        return query
