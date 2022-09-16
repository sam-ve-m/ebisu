# Ebisu
from src.domain.validators.forex_exchange.currency_options import CurrencyExchange, CurrencyOptions
from src.domain.enums.forex_exchange.nature_operation import NatureOperation
from src.domain.exceptions.domain.forex_exchange.exception import (
    InvalidOperation, SpreadTaxNotFound, OperationNotImplemented
)

# Third party
from decouple import config


class CustomerExchangeRequestModel:
    def __init__(self, customer_exchange_data: dict, payload: CurrencyExchange, exchange_account_id: int):
        self.base = payload.base
        self.exchange_account_id = exchange_account_id
        self.quote = payload.quote
        self.quantity = payload.quantity
        self.operation_key = self.__get_operation_value()
        self.spread = self.__get_spread_tax(customer_exchange_data=customer_exchange_data)

    async def build_url_path_to_request_current_currency_quote(self) -> str:
        map_url_path = {
            NatureOperation.BRL_TO_USD: f'{config("BASE_URL_FROM_EXCHANGE_API")}/{config("CURRENT_CURRENCY_QUOTE_URL").format(self.operation_key.value, CurrencyOptions.BRL, CurrencyOptions.USD, self.exchange_account_id, self.spread)}',
            NatureOperation.USD_TO_BRL: f'{config("BASE_URL_FROM_EXCHANGE_API")}/{config("CURRENT_CURRENCY_QUOTE_URL").format(self.operation_key.value, CurrencyOptions.USD, CurrencyOptions.BRL, self.exchange_account_id, self.spread)}',
        }
        url_path = map_url_path.get(self.operation_key)
        if not url_path:
            raise OperationNotImplemented()
        return url_path

    def __get_operation_value(self) -> NatureOperation:
        operation_key = f'{self.base}_TO_{self.quote}'
        map_of_operation_compositions = {
            "BRL_TO_USD": NatureOperation.BRL_TO_USD,
            "USD_TO_BRL": NatureOperation.USD_TO_BRL,
        }
        operation_value = map_of_operation_compositions.get(operation_key)
        if not operation_value:
            raise InvalidOperation()
        return operation_value

    async def get_body_template_to_request_exchange_simulation(self, customer_token: str) -> dict:
        body = {
            "quantidadeMoedaBase": self.quantity,
            "token": customer_token
        }
        return body

    @staticmethod
    def __get_spread_tax(customer_exchange_data: dict) -> float:
        spread = customer_exchange_data.get("spread")
        if not spread:
            raise SpreadTaxNotFound()
        return spread

    @staticmethod
    async def get_url_path_to_request_exchange_simulation() -> str:
        url_path = f'{config("BASE_URL_FROM_EXCHANGE_API")}/{config("EXCHANGE_SIMULATION_URL")}'
        return url_path
