from typing import List
from src.domain.enums.order_status import OrderStatus
from src.repositories.orders.br.repository import BrOrdersRepository


class GetBrOrders:
    oracle_singleton_instance = BrOrdersRepository

    @staticmethod
    def build_query(
        accounts: List[str],
        offset: int,
        limit: int,
        order_status: List[OrderStatus],
    ) -> str:
        query = f"""SELECT B.SYMBOL, B.ROOTCLORDID, B.ORDSTATUS, B.CLORDID, B.CREATEDAT, B.CUMQTY, B.AVGPX, B.ORDTYPE, B.ORDERQTY, B.SIDE, B.PRICE, B.STOPPX
                FROM UORDEDB001.VW_ORDER_LIST B
                WHERE B.ACCOUNT in ('{"','".join(accounts)}')
                {GetBrOrders.filter(order_status)} order by CREATEDAT DESC offset {offset} rows fetch first {limit} row only"""
        return query

    @staticmethod
    def build_quantity_query(
        accounts: List[str],
        order_status: List[OrderStatus],
    ) -> str:

        query = f"""SELECT count(*) as count
                        FROM UORDEDB001.VW_ORDER_LIST B
                        WHERE B.ACCOUNT in ('{"','".join(accounts)}')
                        {GetBrOrders.filter(order_status)}
                        ORDER BY B.TRANSACTTIME DESC
                        """
        return query

    @staticmethod
    def build_client_orders_query(accounts: List[str], root_cl_order_id: str) -> str:
        query = f"""SELECT C.MESSAGE, A.*
                        FROM UORDEDB001.VW_ORDER_DETAILS A
                        LEFT JOIN UORDEDB001.MAP_ORDERS_REJECT_REASON_TO_SIGAME_MESSAGES B ON A.ORDREJREASON = B.B3_MESSAGE_ID
                        LEFT JOIN UORDEDB001.SIGAME_ORDERS_MESSAGES C ON B.SIGAME_MESSAGE_ID = C.SIGAME_MESSAGE_ID
                        WHERE ACCOUNT in ('{"', '".join(accounts)}') AND ROOTCLORDID = '{root_cl_order_id}'
                        ORDER BY CREATEDAT DESC
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
