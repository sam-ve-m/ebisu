# Ebisu
from src.domain.validators.forex_exchange.currency_options import CurrencyExchange
from src.domain.enums.forex_exchange import NatureOperation
from src.domain.exceptions.domain.forex_exchange.exception import InvalidOperation, MissingExchangeAccountId, MissingSpreadTax

# Third party
from decouple import config


class ProposalSimulationModel:
    def __init__(self, user_exchange_data: dict, currency_exchange: CurrencyExchange):
        self.currency_exchange = currency_exchange
        self.user_exchange_data = user_exchange_data
        self.exchange_account_id = self._get_exchange_account_id()
        self.spread = self._get_spread_tax()
        self.operation_key = self._get_operation_value()

    async def build_url_path_to_current_currency_quote(self):
        map_url_path = {
            4: f'{config("BASE_URL")}/{self.operation_key}/taxa/BRL/USD/cliente/{self.exchange_account_id}/spread/'
               f'{self.spread}',
            54: f'{config("BASE_URL")}/{self.operation_key}/taxa/USD/BRL/cliente/{self.exchange_account_id}/spread/'
                f'{self.spread}',
        }
        url_path = map_url_path.get(self.operation_key)
        return url_path

    def _get_operation_value(self) -> int | InvalidOperation:
        operation_key = f'{self.currency_exchange.base}_TO_{self.currency_exchange.quote}'
        map_of_operation_compositions = {
            "BRL_TO_USD": NatureOperation.BRL_TO_USD.value,
            "USD_TO_BRL": NatureOperation.USD_TO_BRL.value,
        }
        operation_value = map_of_operation_compositions.get(operation_key)
        if not operation_value:
            raise InvalidOperation
        return operation_value

    def _get_exchange_account_id(self) -> str | MissingExchangeAccountId:
        exchange_account_id = self.user_exchange_data.get("exchange_account_id")
        if not exchange_account_id:
            raise MissingExchangeAccountId
        return exchange_account_id

    def _get_spread_tax(self) -> float | MissingSpreadTax:
        spread = self.user_exchange_data.get("spread")
        if not spread:
            raise MissingSpreadTax
        return spread


"https://sbxapi.ourinvest.com.br:43400/api/v1/produto/cambio/naturezaOperacao/4/taxa/BRL/USD/cliente/208785/spread/0.02"
