# Ebisu
from src.domain.enums.forex.liquidation_date import LiquidationDayOptions
from src.domain.enums.forex.countrys import Country
from src.domain.enums.forex.composition_hash_options import Balance, Wallet
from src.domain.enums.forex.operations import OperationType
from src.domain.enums.forex.time_zones import TimeZones
from src.domain.exceptions.domain.model.forex.model import (
    InvalidRedisHashCombination,
    ErrorGettingValueByExchangeHash,
)
from src.domain.date_formatters.region.date_time.model import RegionDateFormat
from src.domain.models.forex.markets.calendar.model import ForexMarketCalendars
from src.domain.models.forex.markets.liga_invest_markets.model import LigaInvestStock
from src.domain.models.thebes_answer.model import ThebesAnswer
from src.domain.models.forex.proposal.simulation_token.model import SimulationTokenModel
from src.domain.request.forex.execution_proposal import ForexSimulationToken
from src.infrastructures.env_config import config

# Third party
from datetime import datetime
from halberd import Country as HalberdCountry


class ExecutionModel:
    def __init__(
        self,
        payload: ForexSimulationToken,
        thebes_answer: ThebesAnswer,
        token_decoded: dict,
        account_number: int,
    ):
        self.thebes_answer = thebes_answer
        self.thebes_answer.account_br_is_blocked()
        self.stock_market = LigaInvestStock(
            date_time=datetime.now(tz=TimeZones.BR_SP.value),
            time_zone=TimeZones.BR_SP,
            market_calendar=ForexMarketCalendars(nyse=True, bmf=True),
        )
        self.token = payload.proposal_simulation_token

        self.token_decoded = SimulationTokenModel(token_decoded=token_decoded)
        self.account_number = account_number
        self.exchange_proposal_value = self.__get_exchange_proposal_value()
        self.next_d2 = self.stock_market.get_liquidation_date(
            day=LiquidationDayOptions.D2
        ).strftime(RegionDateFormat.BR_DATE_ZULU_FORMAT.value)
        self.operation_type = self.__get_operation_type()
        self.redis_hash = self.get_redis_hash()
        self.origin_country = self.__get_origin_country()
        self.origin_account = self.__get_origin_account()
        self.halberd_country = self.__get_halberd_country()
        self.destination_country = self.__get_destination_country()
        self.destination_account = self.__get_destination_account()

    def __get_exchange_proposal_value(self) -> float:
        map_exchange_proposal_value_per_hash = {
            "BRL_TO_USD": self.token_decoded.net_value,
            "USD_TO_BRL": self.token_decoded.quantity_currency_traded,
        }
        exchange_proposal_value = map_exchange_proposal_value_per_hash.get(
            self.token_decoded.exchange_hash
        )
        if not exchange_proposal_value:
            raise ErrorGettingValueByExchangeHash()
        return exchange_proposal_value

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
            "BRL_TO_USD": self.thebes_answer.bmf_account,
            "USD_TO_BRL": self.thebes_answer.dw_account,
        }
        origin_account = map_accounts_per_hash.get(self.token_decoded.exchange_hash)
        if not origin_account:
            raise ErrorGettingValueByExchangeHash()
        return origin_account

    def __get_destination_account(self) -> str:
        map_accounts_per_hash = {
            "BRL_TO_USD": self.thebes_answer.dw_account,
            "USD_TO_BRL": self.thebes_answer.bmf_account,
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
            OperationType.USD_TO_BRL: f"{self.thebes_answer.unique_id}:{Country.US.lower()}:{self.thebes_answer.dw_account}:{Wallet.BALANCE}:"
            f"{Balance.ALLOWED_TO_WITHDRAW}:*",
            OperationType.BRL_TO_USD: f"{self.thebes_answer.unique_id}:{Country.BR.lower()}:{self.thebes_answer.bmf_account}:{Wallet.BALANCE}:"
            f"{Balance.ALLOWED_TO_WITHDRAW}:*",
        }
        redis_hash = hash_map.get(self.operation_type)
        if not redis_hash:
            raise InvalidRedisHashCombination()
        return redis_hash

    def get_bifrost_template_ted_to_forex(self) -> dict:
        bifrost_template = {
            "origin_account": {
                "user_unique_id": self.thebes_answer.unique_id,
                "account_number": self.origin_account,
                "country": self.origin_country,
            },
            "account_destination": {
                "user_unique_id": self.thebes_answer.unique_id,
                "account_number": self.account_number,
                "country": self.destination_country,
            },
            "value": self.token_decoded.net_value,
        }
        return bifrost_template

    def get_bifrost_template_to_buy_power(self) -> dict:
        bifrost_template = {
            "origin_account": {
                "user_unique_id": self.thebes_answer.unique_id,
                "account_number": self.origin_account,
                "country": self.origin_country,
            },
            "account_destination": {
                "user_unique_id": self.thebes_answer.unique_id,
                "account_number": self.destination_account,
                "country": self.destination_country,
            },
            "value": self.token_decoded.quantity_currency_traded,
        }
        return bifrost_template

    def get_bifrost_template_to_withdraw(self) -> dict:
        bifrost_template = {
            "origin_account": {
                "user_unique_id": self.thebes_answer.unique_id,
                "account_number": self.origin_account,
                "country": self.origin_country,
            },
            "account_destination": {
                "user_unique_id": self.thebes_answer.unique_id,
                "account_number": self.destination_account,
                "country": self.destination_country,
            },
            "value": self.token_decoded.net_value,
        }
        return bifrost_template

    def get_execute_proposal_body(self, customer_data: dict) -> dict:
        next_d2_date_time_formatted = self.next_d2
        name = customer_data.get("name")
        out_body = {
            "token": self.token,
            "dadosBeneficiario": {
                "siglaPaisBanco": Country.US,
                "nomeBanco": config("BENEFICIARY_BANK_NAME"),
                "codigoSWIFTBanco": config("BENEFICIARY_SWIFT_BANK_CODE"),
                "nomeBeneficiario": config("BENEFICIARY_NAME"),
                "contaBeneficiario": config("BENEFICIARY_ACCOUNT"),
                "infoComplementar": f"/{self.thebes_answer.dw_display_account}/{name}"
            },
            "dataLiquidacaoFutura": next_d2_date_time_formatted,
        }

        in_body = {
            "token": self.token,
            "dadosContaRecebimento": {
                "codigoAgencia": config("LIGA_AGENCY_NUMBER"),
                "codigoBanco": config("LIGA_BANK_CODE"),
                "codigoConta": self.thebes_answer.bmf_account,
                "digitoConta": self.thebes_answer.bmf_account_digit,
            },
            "dataLiquidacaoFutura": self.next_d2,
        }

        map_execute_body = {
            "BRL_TO_USD": out_body,
            "USD_TO_BRL": in_body,
        }

        body = map_execute_body.get(self.token_decoded.exchange_hash)

        return body

    @staticmethod
    def get_execution_url() -> str:
        url_path = f'{config("BASE_URL_FROM_EXCHANGE_API")}/{config("EXECUTION_URL")}'
        return url_path
