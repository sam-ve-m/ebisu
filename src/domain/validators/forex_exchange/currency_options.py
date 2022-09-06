# Ebisu
from src.domain.enums.forex_exchange import CurrencyOptions

# Third party
from pydantic import BaseModel


class CurrencyExchange(BaseModel):
    base: CurrencyOptions
    quote: CurrencyOptions
    quantity: float
