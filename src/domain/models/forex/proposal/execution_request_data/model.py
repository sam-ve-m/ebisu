# Ebisu
from datetime import datetime

from src.domain.enums.forex.liquidation_date import LiquidationDayOptions
from src.domain.enums.forex.countrys import Country
from src.domain.enums.forex.composition_hash_options import Balance, Wallet
from src.domain.enums.forex.operations import OperationType
from src.domain.enums.forex.time_zones import TimeZones
from src.domain.exceptions.domain.forex.exception import (
    InvalidRedisHashCombination,
    ErrorGettingValueByExchangeHash,
)
from src.domain.date_formatters.region.date_time.model import RegionDateFormat
from src.domain.models.forex.markets.calendar.model import ForexMarketCalendars
from src.domain.models.forex.markets.liga_invest_markets.model import LigaInvestStock
from src.domain.models.forex.proposal.simulation_token.model import SimulationTokenModel
from src.domain.models.jwt_user_data.model import JwtModel
from src.domain.validators.forex.execution_proposal import ForexSimulationToken
from src.infrastructures.env_config import config
from halberd import Country as HalberdCountry


class ExecutionModel:
    def __init__(
        self,
        payload: ForexSimulationToken,
        jwt_data: dict,
        token_decoded: dict,
        account_number: int,
    ):
        self.jwt = JwtModel(jwt_data=jwt_data)
        self.stock_market = LigaInvestStock(
            date_time=datetime.now(tz=TimeZones.BR_SP.value),
            time_zone=TimeZones.BR_SP,
            market_calendar=ForexMarketCalendars(nyse=True, bmf=True),
        )
        self.token = payload.proposal_simulation_token
        self.token_decoded = SimulationTokenModel(token_decoded=token_decoded)
        self.account_number = account_number
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
        destination_account = map_accounts_per_hash.get(
            self.token_decoded.exchange_hash
        )
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
        destination_country = map_countries_per_hash.get(
            self.token_decoded.exchange_hash
        )
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

    def get_bifrost_template_ted_to_forex(self) -> dict:
        bifrost_template = {
            "origin_account": {
                "user_unique_id": self.jwt.unique_id,
                "account_number": self.origin_account,
                "country": self.origin_country,
            },
            "account_destination": {
                "user_unique_id": self.jwt.unique_id,
                "account_number": self.account_number,
                "country": self.destination_country,
            },
            "value": self.token_decoded.net_value,
        }
        return bifrost_template

    def get_bifrost_template_to_buy_power(self) -> dict:
        bifrost_template = {
            "origin_account": {
                "user_unique_id": self.jwt.unique_id,
                "account_number": self.origin_account,
                "country": self.origin_country,
            },
            "account_destination": {
                "user_unique_id": self.jwt.unique_id,
                "account_number": self.destination_account,
                "country": self.destination_country,
            },
            "value": self.token_decoded.quantity_currency_traded,
        }
        return bifrost_template

    def get_bifrost_template_to_withdraw(self) -> dict:
        bifrost_template = {
            "origin_account": {
                "user_unique_id": self.jwt.unique_id,
                "account_number": self.origin_account,
                "country": self.origin_country,
            },
            "account_destination": {
                "user_unique_id": self.jwt.unique_id,
                "account_number": self.destination_account,
                "country": self.destination_country,
            },
            "value": self.token_decoded.net_value,
        }
        return bifrost_template

    def get_execute_proposal_body(self, customer_data: dict) -> dict:
        next_d2 = self.stock_market.get_liquidation_date(day=LiquidationDayOptions.D2)
        next_d2_date_time_formatted = next_d2.strftime(
            RegionDateFormat.BR_DATE_ZULU_FORMAT.value
        )
        name = customer_data.get("name")

        body = {
            "token": self.token,
            "dadosBeneficiario": {
                "siglaPaisBanco": Country.US,
                "nomeBanco": config("BENEFICIARY_BANK_NAME"),
                "codigoSWIFTBanco": config("BENEFICIARY_SWIFT_BANK_CODE"),
                "nomeBeneficiario": config("BENEFICIARY_NAME"),
                "contaBeneficiario": config("BENEFICIARY_ACCOUNT"),
                "infoComplementar": f"/{self.origin_account}/{name}",
            },
            "dataLiquidacaoFutura": next_d2_date_time_formatted,
        }
        return body

    @staticmethod
    def get_execution_url() -> str:
        url_path = f'{config("BASE_URL_FROM_EXCHANGE_API")}/{config("EXECUTION_URL")}'
        return url_path
