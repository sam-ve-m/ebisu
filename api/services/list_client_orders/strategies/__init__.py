from api.services.list_client_orders.strategies.br_orders.strategy import GetBrOrders
from api.services.list_client_orders.strategies.us_orders.strategy import GetUsOrders
from api.domain.enums.region import Region

order_region = {
    Region.BR.value: GetBrOrders,
    Region.US.value: GetUsOrders,
}
