# imports
from src.services.earnings_from_client.strategies.br import GetBrEarningsDetails


earnings_client_region = {"BR": GetBrEarningsDetails, "US": "GetUsEarningsDetails"}
