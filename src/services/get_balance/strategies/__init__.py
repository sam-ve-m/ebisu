from src.services.get_balance.strategies.br.strategy import GetBrBalance
from src.services.get_balance.strategies.us.strategy import GetUsBalance

balance_region = {
    "BR": GetBrBalance,
    "US": GetUsBalance,
}
