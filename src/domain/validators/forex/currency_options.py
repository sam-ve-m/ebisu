# Ebisu
from src.domain.enums.forex.currency import CurrencyOptions

# Third party
from pydantic import BaseModel


class CurrencyExchange(BaseModel):
    base: CurrencyOptions
    quote: CurrencyOptions
    quantity: float
