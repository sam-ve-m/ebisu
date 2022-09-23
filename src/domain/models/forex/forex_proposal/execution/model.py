# Ebisu
from src.domain.enums.forex.liquidation_date import LiquidationDayOptions
from src.domain.enums.forex.countrys import Country
from src.domain.validators.forex.execution_proposal import ForexExecution
from src.domain.date_formatters.region.date_time.model import RegionDateFormat


class JwtUserData:
    def __init__(self, jwt_data: dict):
        self.jwt_data = jwt_data
        self.unique_id = self.__get_unique_id()
        self.portfolios = self.__get_portfolios()
        self.bovespa_account = self.__get_bovespa_account()
        self.dw_account = self.__get_dw_account()
        self.dw_display_account = self.__get_dw_display_account()

    def __get_bovespa_account(self):
        bovespa_account = self.portfolios.get("br", {}).get("bovespa_account")
        if not bovespa_account:
            raise Exception
        return bovespa_account

    def __get_dw_account(self):
        dw_account = self.portfolios.get("us", {}).get("dw_account")
        if not dw_account:
            raise Exception
        return dw_account

    def __get_dw_display_account(self):
        dw_display_account = self.portfolios.get("us", {}).get("dw_display_account")
        if not dw_display_account:
            raise Exception
        return dw_display_account

    def __get_portfolios(self):
        portfolios = self.jwt_data.get("user_exchange", {}).get("unique_id", {}).get("portfolios")
        if not portfolios:
            raise Exception
        return portfolios

    def __get_unique_id(self):
        unique_id = self.jwt_data.get("user_exchange", {}).get("unique_id")
        if not unique_id:
            raise Exception
        return unique_id


class ProposalTokenData:
    def __init__(self, token_decoded: dict):
        self.token_decoded = token_decoded
        self.net_value = self.__get_net_value()

    def __get_net_value(self):
        net_value = self.token_decoded.get("ValorLiquido")
        if not net_value:
            raise Exception
        return net_value

    def __get_nature_operation(self):
        nature_operation = self.token_decoded.get("CodigoNaturezaOperacao")
        if not nature_operation:
            raise Exception
        return nature_operation


class ExecutionProposalModel:
    def __init__(self, payload: ForexExecution, jwt_data: dict, token_decoded: dict):
        self.proposal_token_encoded = payload.customer_proposal_token
        self.stock_market = payload.liga_invest_stock_market
        self.proposal_token_data_decoded = ProposalTokenData(token_decoded=token_decoded)
        self.jwt = JwtUserData(jwt_data=jwt_data)

    def get_bifrost_template_brl_to_usd(self) -> dict:
        out_template = {
            "origin_account": {
                "user_unique_id": self.jwt.unique_id,
                "account_number": self.jwt.bovespa_account,
                "country": Country.BR
            },
            "account_destination": {
                "user_unique_id": self.jwt.unique_id,
                "account_number": self.jwt.dw_account,
                "country": Country.US
            },
            "value": self.proposal_token_data_decoded.net_value
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
                "account_number": self.jwt.bovespa_account,
                "country": Country.BR
            },
            "value": self.proposal_token_data_decoded.net_value
        }
        return in_template

    def get_template_body_execute_proposal(self, nick_name: str) -> dict:
        next_d2 = self.stock_market.get_liquidation_date(day=LiquidationDayOptions.D2)
        next_d2_date_time_formatted = next_d2.strftime(RegionDateFormat.BR_DATE_ZULU_FORMAT.value)
        request_date_time_formatted = self.stock_market.date_time.strftime(RegionDateFormat.BR_DATE_ZULU_FORMAT.value)

        template = {
            "token": self.proposal_token_encoded,
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

        return template

