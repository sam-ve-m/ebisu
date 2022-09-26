# Ebisu
from src.domain.enums.forex.liquidation_date import LiquidationDayOptions
from src.domain.enums.forex.countrys import Country
from src.domain.enums.forex.composition_hash_options import Balance, Wallet
from src.domain.enums.forex.operations import OperationType, HalberdCountry
from src.domain.exceptions.domain.forex_exchange.exception import InvalidOperation, InvalidHashCombination
from src.domain.models.jwt_user_data.model import JwtModel
from src.domain.validators.forex.execution_proposal import ForexExecution
from src.domain.date_formatters.region.date_time.model import RegionDateFormat


class ProposalTokenData:
    def __init__(self, token_decoded: dict):
        self.token_decoded = token_decoded
        self.exchange_account_id = self.__get_exchange_account_id()
        self.exchange_hash = self.__get_exchange_combination_hash()
        self.halberd_country = self.__get_halberd_country()
        self.nature_operation = self.__get_nature_operation()
        self.net_value = self.__get_net_value()
        self.operation_type = self.__get_operation_type()

    def __get_exchange_account_id(self):
        exchange_account_id = self.token_decoded.get("CodigoCliente")
        if not exchange_account_id:
            raise Exception
        return exchange_account_id

    def __get_net_value(self):
        net_value = self.token_decoded.get("ValorLiquido")
        if not net_value:
            raise Exception
        return net_value

    def __get_nature_operation(self):
        nature_operation = self.token_decoded.get("CodigoNaturezaOperacao")
        if not nature_operation:
            raise Exception
        return int(nature_operation)

    def __get_exchange_combination_hash(self):
        base = self.token_decoded.get("SimboloMoedaBase")
        quote = self.token_decoded.get("SimboloMoedaCotacao")
        if not all([base, quote]):
            raise Exception
        exchange_combination_hash = f'{base}_TO_{quote}'
        return exchange_combination_hash

    def __get_operation_type(self):
        map_operation_types_per_hash = {
            "BRL_TO_USD": OperationType.BRL_TO_USD,
            "USD_TO_BRL": OperationType.USD_TO_BRL,
        }
        operation = map_operation_types_per_hash.get(self.exchange_hash)
        if not operation:
            raise InvalidOperation()
        return operation

    def __get_halberd_country(self):
        map_countries_per_hash = {
            "BRL_TO_USD": HalberdCountry.BR,
            "USD_TO_BRL": HalberdCountry.US,
        }
        halberd_country = map_countries_per_hash.get(self.exchange_hash)
        if not halberd_country:
            raise InvalidOperation()
        return halberd_country


class ExecutionProposalModel:
    def __init__(self, payload: ForexExecution, jwt_data: dict, token_decoded: dict):
        self.jwt = JwtModel(jwt_data=jwt_data)
        self.token = payload.customer_proposal_token
        self.token_decoded = ProposalTokenData(token_decoded=token_decoded)
        self.stock_market = payload.liga_invest_stock_market
        self.balance_hash = self.get_balance_hash()

    def get_balance_hash(self):
        hash_map = {
            OperationType.USD_TO_BRL: f"{self.jwt.unique_id}:{Country.US.lower()}:{self.jwt.dw_account}:{Wallet.BALANCE}:"
                                      f"{Balance.ALLOWED_TO_WITHDRAW}:*",
            OperationType.BRL_TO_USD: f"{self.jwt.unique_id}:{Country.BR.lower()}:{self.jwt.bmf_account}:{Wallet.BALANCE}:"
                                      f"{Balance.ALLOWED_TO_WITHDRAW}:*",
        }
        balance_hash = hash_map.get(self.token_decoded.operation_type)
        if not balance_hash:
            raise InvalidHashCombination()
        return balance_hash

    def get_bifrost_template_brl_to_usd(self) -> dict:
        out_template = {
            "origin_account": {
                "user_unique_id": self.jwt.unique_id,
                "account_number": self.jwt.bmf_account,
                "country": Country.BR
            },
            "account_destination": {
                "user_unique_id": self.jwt.unique_id,
                "account_number": self.jwt.dw_account,
                "country": Country.US
            },
            "value": self.token_decoded.net_value
        }
        return out_template

    def get_bifrost_template_usd_to_brl(self) -> dict:
        in_template = {
            "origin_account": {
                "user_unique_id": self.jwt.unique_id,
                "account_number": self.jwt.dw_account,
                "country": Country.US
            },
            "account_destination": {
                "user_unique_id": self.jwt.unique_id,
                "account_number": self.jwt.bmf_account,
                "country": Country.BR
            },
            "value": self.token_decoded.net_value
        }
        return in_template

    def get_execute_proposal_body(self, nick_name: str) -> dict:
        next_d2 = self.stock_market.get_liquidation_date(day=LiquidationDayOptions.D2)
        next_d2_date_time_formatted = next_d2.strftime(RegionDateFormat.BR_DATE_ZULU_FORMAT.value)
        request_date_time_formatted = self.stock_market.date_time.strftime(RegionDateFormat.BR_DATE_ZULU_FORMAT.value)

        body = {
            "token": self.token,
            "dadosBeneficiario": {
                "siglaPaisBanco": Country.US,
                "nomeBanco": "JPMorgan Chase Bank, National Association",
                "codigoSWIFTBanco": "CHASUS33",
                "nomeBeneficiario": "DriveWealth LLC",
                "contaBeneficiario": "10000337256168",
                "infoComplementar": f"/{self.jwt.dw_display_account}/{nick_name}"
            },
            "dataLiquidacaoFutura": next_d2_date_time_formatted,  # f"{date}T00:00:00.000Z"
            "controle": {
                "dataHoraCliente": request_date_time_formatted,
                "byPassTokenRefresh": True,
                "recurso": {
                    "codigo": "63",
                    "sigla": "CAAS"
                },
                "origem": {
                    "nome": "SmartCambio.ClientAPI.LIONX",
                    "chave": "SYSTEM::API::KEY::LIONX",
                    "endereco": "IP_NOSSO_QUE_ESTA_FAZENDO_A_REQUISIÇÃO",
                }
            }
        }
        return body




