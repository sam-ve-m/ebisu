from typing import List
from src.domain.enums.order_status import OrderStatus
from src.repositories.orders.br.repository import BrOrdersRepository


class GetBrOrders:
    oracle_singleton_instance = BrOrdersRepository

    @staticmethod
    def build_query(
        accounts: List[str],
        order_status: List[OrderStatus],
    ) -> str:

        query = f"""SELECT count(*) as count
                    FROM USOLUDB001.VW_CURRENT_EXECUTION_REPORTS B
                    WHERE B.ACCOUNT in ('{"','".join(accounts)}')
                    {GetBrOrders.filter(order_status)}
                    ORDER BY B.TRANSACTTIME DESC
                    """
        return query

    @staticmethod
    def filter(order_status: List[OrderStatus]):

        if not order_status:
            filter_order_status = ""
            return filter_order_status

        order_status = [status.value for status in order_status]
        if len(order_status) > 1:
            filter_order_status = "AND B.ORDSTATUS in " + str(tuple(order_status))
        else:
            filter_order_status = f"AND B.ORDSTATUS = '{order_status.pop()}'"
        return filter_order_status
