from src.services.get_client_orders.strategies.br_orders.strategy import (
    GetBrOrdersDetails,
)
from src.services.get_client_orders.strategies.us_orders.strategy import (
    GetUsOrdersDetails,
)

order_region = {"BR": GetBrOrdersDetails, "US": GetUsOrdersDetails}
