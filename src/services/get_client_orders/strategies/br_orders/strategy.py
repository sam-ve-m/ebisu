from src.repositories.orders.br.repository import BrOrdersRepository
from typing import List


class GetBrOrdersDetails:

    oracle_singleton_instance = BrOrdersRepository

    @staticmethod
    def build_query(accounts: List[str], root_cl_order_id: str) -> str:
        query = f"""SELECT C.MESSAGE, A.*
                    FROM UORDEDB001.VW_ORDER_DETAILS A
                    LEFT JOIN UORDEDB001.MAP_ORDERS_REJECT_REASON_TO_SIGAME_MESSAGES B ON A.ORDREJREASON = B.B3_MESSAGE_ID
                    LEFT JOIN UORDEDB001.SIGAME_ORDERS_MESSAGES C ON B.SIGAME_MESSAGE_ID = C.SIGAME_MESSAGE_ID
                    WHERE ACCOUNT in ('{"', '".join(accounts)}') AND ROOTCLORDID = '{root_cl_order_id}'
                    ORDER BY CREATEDAT DESC
                    """
        return query
