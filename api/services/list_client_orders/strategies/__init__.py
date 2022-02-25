from api.services.list_client_orders.strategies.br_orders.strategy import GetBrOrders
from api.services.list_client_orders.strategies.us_orders.strategy import GetUsOrders

order_region = {
        "BR": GetBrOrders,
        "US": GetUsOrders,
    }

