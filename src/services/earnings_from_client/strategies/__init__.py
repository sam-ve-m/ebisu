# imports
from src.services.earnings_from_client.strategies.br import GetBrEarningsDetails
from src.services.earnings_from_client.strategies.us import GetUsEarningsDetails

earnings_client_region = {"BR": GetBrEarningsDetails,
                          "US": GetUsEarningsDetails}
