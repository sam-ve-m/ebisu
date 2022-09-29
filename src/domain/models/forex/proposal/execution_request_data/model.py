# Ebisu
from src.domain.enums.forex.liquidation_date import LiquidationDayOptions
from src.domain.enums.forex.countrys import Country
from src.domain.enums.forex.composition_hash_options import Balance, Wallet
from src.domain.enums.forex.operations import OperationType
from src.domain.exceptions.domain.forex.exception import (
    InvalidRedisHashCombination, DataNotFoundInToken, ErrorGettingValueByExchangeHash
)
from src.domain.date_formatters.region.date_time.model import RegionDateFormat
from src.domain.models.jwt_user_data.model import JwtModel
from src.domain.validators.forex.execution_proposal import ForexExecution
from src.infrastructures.env_config import config
from halberd import Country as HalberdCountry


class ProposalTokenData:
    def __init__(self, token_decoded: dict):
        self.token_decoded = token_decoded
        self.forex_account = self.__get_forex_account()
        self.exchange_hash = self.__get_exchange_combination_hash()
        self.nature_operation = self.__get_nature_operation()
        self.net_value = self.__get_net_value()

    def __get_forex_account(self):
        forex_account = self.token_decoded.get("CodigoCliente")
        if not forex_account:
            raise DataNotFoundInToken()
        return forex_account

    def __get_net_value(self):
        net_value = self.token_decoded.get("ValorLiquido")
        if not net_value:
            raise DataNotFoundInToken()
        return float(net_value)

    def __get_nature_operation(self):
        nature_operation = self.token_decoded.get("CodigoNaturezaOperacao")
        if not nature_operation:
            raise DataNotFoundInToken()
        return int(nature_operation)

    def __get_exchange_combination_hash(self):
        base = self.token_decoded.get("SimboloMoedaBase")
        quote = self.token_decoded.get("SimboloMoedaCotacao")
        if not all([base, quote]):
            raise DataNotFoundInToken()
        exchange_combination_hash = f'{base}_TO_{quote}'
        return exchange_combination_hash


class ExecutionModel:
    def __init__(self, payload: ForexExecution, jwt_data: dict, token_decoded: dict):
        self.jwt = JwtModel(jwt_data=jwt_data)
        self.stock_market = payload.liga_invest_stock_market
        self.token = payload.proposal_simulation_token
        self.token_decoded = ProposalTokenData(token_decoded=token_decoded)
        self.operation_type = self.__get_operation_type()
        self.redis_hash = self.get_redis_hash()
        self.origin_country = self.__get_origin_country()
        self.origin_account = self.__get_origin_account()
        self.halberd_country = self.__get_halberd_country()
        self.destination_country = self.__get_destination_country()
        self.destination_account = self.__get_destination_account()

    def __get_operation_type(self) -> OperationType:
        map_operation_types_per_hash = {
            "BRL_TO_USD": OperationType.BRL_TO_USD,
            "USD_TO_BRL": OperationType.USD_TO_BRL,
        }
        operation = map_operation_types_per_hash.get(self.token_decoded.exchange_hash)
        if not operation:
            raise ErrorGettingValueByExchangeHash()
        return operation

    def __get_origin_account(self) -> str:
        map_accounts_per_hash = {
            "BRL_TO_USD": self.jwt.bmf_account,
            "USD_TO_BRL": self.jwt.dw_account,
        }
        origin_account = map_accounts_per_hash.get(self.token_decoded.exchange_hash)
        if not origin_account:
            raise ErrorGettingValueByExchangeHash()
        return origin_account

    def __get_destination_account(self) -> str:
        map_accounts_per_hash = {
            "BRL_TO_USD": self.jwt.dw_account,
            "USD_TO_BRL": self.jwt.bmf_account,
        }
        destination_account = map_accounts_per_hash.get(self.token_decoded.exchange_hash)
        if not destination_account:
            raise ErrorGettingValueByExchangeHash()
        return destination_account

    def __get_origin_country(self) -> Country:
        map_countries_per_hash = {
            "BRL_TO_USD": Country.BR,
            "USD_TO_BRL": Country.US,
        }
        origin_country = map_countries_per_hash.get(self.token_decoded.exchange_hash)
        if not origin_country:
            raise ErrorGettingValueByExchangeHash()
        return origin_country

    def __get_halberd_country(self) -> Country:
        map_countries_per_hash = {
            "BRL_TO_USD": HalberdCountry.BR,
            "USD_TO_BRL": HalberdCountry.US,
        }
        origin_country = map_countries_per_hash.get(self.token_decoded.exchange_hash)
        if not origin_country:
            raise ErrorGettingValueByExchangeHash()
        return origin_country

    def __get_destination_country(self) -> Country:
        map_countries_per_hash = {
            "BRL_TO_USD": Country.US,
            "USD_TO_BRL": Country.BR,
        }
        destination_country = map_countries_per_hash.get(self.token_decoded.exchange_hash)
        if not destination_country:
            raise ErrorGettingValueByExchangeHash()
        return destination_country

    def get_redis_hash(self) -> str:
        hash_map = {
            OperationType.USD_TO_BRL: f"{self.jwt.unique_id}:{Country.US.lower()}:{self.jwt.dw_account}:{Wallet.BALANCE}:"
                                      f"{Balance.ALLOWED_TO_WITHDRAW}:*",
            OperationType.BRL_TO_USD: f"{self.jwt.unique_id}:{Country.BR.lower()}:{self.jwt.bmf_account}:{Wallet.BALANCE}:"
                                      f"{Balance.ALLOWED_TO_WITHDRAW}:*",
        }
        redis_hash = hash_map.get(self.operation_type)
        if not redis_hash:
            raise InvalidRedisHashCombination()
        return redis_hash

    def get_bifrost_template(self) -> dict:
        bifrost_template = {
            "origin_account": {
                "user_unique_id": self.jwt.unique_id,
                "account_number": self.origin_account,
                "country": self.origin_country
            },
            "account_destination": {
                "user_unique_id": self.jwt.unique_id,
                "account_number": self.destination_account,
                "country": self.destination_country,
            },
            "value": self.token_decoded.net_value
        }
        return bifrost_template

    def get_execute_proposal_body(self, customer_data: dict) -> dict:
        next_d2 = self.stock_market.get_liquidation_date(day=LiquidationDayOptions.D2)
        next_d2_date_time_formatted = next_d2.strftime(RegionDateFormat.BR_DATE_ZULU_FORMAT.value)
        name = customer_data.get("name")

        body = {
            "token": self.token,
            "dadosBeneficiario": {
                "siglaPaisBanco": Country.US,
                "nomeBanco": "JPMorgan Chase Bank, National Association",
                "codigoSWIFTBanco": "CHASUS33",
                "nomeBeneficiario": "DriveWealth LLC",
                "contaBeneficiario": "10000337256168",
                "infoComplementar": f"/{self.origin_account}/{name}"
            },
            "dataLiquidacaoFutura": next_d2_date_time_formatted,  # f"{date}T00:00:00.000Z"
        }
        return body

    @staticmethod
    def get_execution_url():
        url_path = f'{config("BASE_URL_FROM_EXCHANGE_API")}/{config("EXECUTION_URL")}'
        return url_path

# jwt_data = {
#   "exp": 1687961421,
#   "created_at": 1656425421.60926,
#   "scope": {
#     "view_type": "default",
#     "user_level": "client",
#     "features": [
#       "default",
#       "realtime"
#     ]
#   },
#   "user": {
#     "unique_id": "40db7fee-6d60-4d73-824f-1bf87edc4491",
#     "nick_name": "RAST3",
#     "portfolios": {
#       "br": {
#         "bovespa_account": "000000014-6",
#         "bmf_account": "14"
#       },
#       "us": {
#         "dw_account": "89c69304-018a-40b7-be5b-2121c16e109e.1651525277006",
#         "dw_display_account": "LX01000001"
#       }
#     },
#     "client_has_br_trade_allowed": True,
#     "client_has_us_trade_allowed": True,
#     "client_profile": "investor"
#   }
# }
#
# token_decoded = {
#   "CodigoCliente": "208785",
#   "CodigoNaturezaOperacao": "4",
#   "SimboloMoedaBase": "BRL",
#   "SimboloMoedaCotacao": "USD",
#   "QuantidadeMoedaNegociada": "46.33",
#   "ValorCotacaoCambio": "5.33770171",
#   "ValorTarifa": "0",
#   "ValorBruto": "247.28",
#   "PercentualIOF": "1.100000",
#   "ValorIOF": "2.72",
#   "ValorLiquido": "250.00",
#   "DataCotacao": "1664477550",
#   "DataValidade": "1664478234",
#   "DataPagamento": "1664431200",
#   "PercentualSpread": "0.0200",
#   "TaxaComercial": "5.2330",
#   "tp": "Rv3mfiTL8sBoqhaOoAJciQ==",
#   "nbf": 1664477550,
#   "exp": 1664478234,
#   "iat": 1664478115,
#   "iss": "208785"
# }
#
# payload = ForexExecution(**{"proposal_simulation_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJDb2RpZ29DbGllbnRlIjoiMjA4Nzg1IiwiQ29kaWdvTmF0dXJlemFPcGVyYWNhbyI6IjQiLCJTaW1ib2xvTW9lZGFCYXNlIjoiQlJMIiwiU2ltYm9sb01vZWRhQ290YWNhbyI6IlVTRCIsIlF1YW50aWRhZGVNb2VkYU5lZ29jaWFkYSI6IjQ2LjMzIiwiVmFsb3JDb3RhY2FvQ2FtYmlvIjoiNS4zMzc3MDE3MSIsIlZhbG9yVGFyaWZhIjoiMCIsIlZhbG9yQnJ1dG8iOiIyNDcuMjgiLCJQZXJjZW50dWFsSU9GIjoiMS4xMDAwMDAiLCJWYWxvcklPRiI6IjIuNzIiLCJWYWxvckxpcXVpZG8iOiIyNTAuMDAiLCJEYXRhQ290YWNhbyI6IjE2NjQ0Nzc1NTAiLCJEYXRhVmFsaWRhZGUiOiIxNjY0NDc4MjM0IiwiRGF0YVBhZ2FtZW50byI6IjE2NjQ0MzEyMDAiLCJQZXJjZW50dWFsU3ByZWFkIjoiMC4wMjAwIiwiVGF4YUNvbWVyY2lhbCI6IjUuMjMzMCIsInRwIjoiUnYzbWZpVEw4c0JvcWhhT29BSmNpUT09IiwibmJmIjoxNjY0NDc3NTUwLCJleHAiOjE2NjQ0NzgyMzQsImlhdCI6MTY2NDQ3ODExNSwiaXNzIjoiMjA4Nzg1In0.Gt5aGm6IBBPBmh6bACAeSRx0plwhcViY5h7QfqrevGM"})
#
#
# a = ExecutionModel(payload=payload, jwt_data=jwt_data, token_decoded=token_decoded)
