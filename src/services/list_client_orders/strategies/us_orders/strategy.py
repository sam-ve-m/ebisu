from typing import List
from src.domain.enums.order_status import OrderStatus
from src.repositories.orders.us.repository import UsOrdersRepository


class GetUsOrders:
    oracle_singleton_instance = UsOrdersRepository

    # TODO: Atualizar para view com root cl order id quando subirmos US
    @staticmethod
    def build_query(
        accounts: List[str],
        offset: int,
        limit: int,
        order_status: List[OrderStatus],
    ) -> str:
        query = f"""SELECT B.SYMBOL, ORDSTATUS, B.CLORDID, B.CREATEDAT, B.CUMQTY, B.AVGPX, B.ORDTYPE, B.ORDERQTY
                    FROM UDRIVDB001.VW_CURRENT_EXECUTION_REPORTS B
                    WHERE B.ACCOUNT in ('{"','".join(accounts)}')
                    {GetUsOrders.filter(order_status)}                   
                    ORDER BY B.CREATEDAT DESC
                    offset {offset} rows
                    fetch first {limit} row only  
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
