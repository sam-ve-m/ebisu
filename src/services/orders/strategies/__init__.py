from src.domain.enums.region import Region
from src.services.orders.strategies.br_orders.strategy import GetBrOrders
from src.services.orders.strategies.us_orders.strategy import GetUsOrders

order_region = {
    Region.BR.value: GetBrOrders,
    Region.US.value: GetUsOrders,
}
