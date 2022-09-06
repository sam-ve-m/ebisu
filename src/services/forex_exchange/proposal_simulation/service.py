# Ebisu
from src.domain.exceptions.service.forex_exchange.exception import (
    UserTokenNotFound, InvalidOperation, ErrorOnGetUserToken, ErrorOnGetExchangeSimulationProposal
)
from src.domain.validators.forex_exchange.currency_options import CurrencyExchange
from src.domain.models.forex_exchange.customer_exchange_request_data.model import CustomerExchangeResquestModel
from src.repositories.user.repository import UserRepository
from caronte import AllowedHTTPMethods, ExchangeCompanyApi

# Standards
from typing import Union


class ProposalSimulationService:

    @classmethod
    async def get_exchange_proposal_simulation(cls, jwt_data: dict, currency_exchange: CurrencyExchange):
        exchange_account_id = jwt_data.get("user", {}).get("exchange_account_id", 208785)
        customer_exchange_data = await cls.__get_customer_exchange_account_data(
            exchange_account_id=exchange_account_id, currency_exchange=currency_exchange
        )
        exchange_proposal_model = CustomerExchangeResquestModel(
            customer_exchange_data=customer_exchange_data,
            currency_exchange=currency_exchange
        )
        customer_token = await cls.__get_customer_token_on_route_21(
            exchange_proposal_model=exchange_proposal_model
        )
        exchange_simulation_proposal_data = await cls.__get_exchange_proposal_values_on_route_22(
            customer_token=customer_token,
        )
        response = await cls.__treatment_exchange_simulation_data(exchange_simulation_proposal_data=exchange_simulation_proposal_data)

    @staticmethod
    async def __treatment_exchange_simulation_data(exchange_simulation_proposal_data: dict):


    @staticmethod
    async def __get_customer_exchange_account_data(exchange_account_id: int, currency_exchange: CurrencyExchange) -> Union[InvalidOperation, dict]:
        customer_exchange_data = await UserRepository.get_user_exchange_data(
            exchange_account_id=exchange_account_id,
            base=currency_exchange.base,
            quote=currency_exchange.quote)
        if not customer_exchange_data:
            raise InvalidOperation()
        return customer_exchange_data

    @staticmethod
    async def __get_customer_token_on_route_21(exchange_proposal_model: CustomerExchangeResquestModel) -> Union[str, UserTokenNotFound, ErrorOnGetUserToken]:
        url_path = await exchange_proposal_model.build_url_path_to_request_current_currency_quote()
        success, caronte_status, content = await ExchangeCompanyApi.request_as_client(
            method=AllowedHTTPMethods.GET,
            url=url_path,
            exchange_account_id=exchange_proposal_model.exchange_account_id
        )
        if not success:
            raise ErrorOnGetUserToken()
        customer_token = content.get("token")
        if not customer_token:
            raise UserTokenNotFound()
        return customer_token

    @staticmethod
    async def __get_exchange_simulation_proposal_on_route_22(customer_token: str, exchange_proposal_model: CustomerExchangeResquestModel) -> Union[dict, ErrorOnGetExchangeSimulationProposal]:
        url_path = await exchange_proposal_model.get_url_path_to_request_exchange_simulation()
        body = await exchange_proposal_model.get_body_template_to_request_exchange_simulation(customer_token=customer_token)
        success, caronte_status, exchange_simulation_proposal_data = ExchangeCompanyApi.request_as_client(
            method=AllowedHTTPMethods.GET,
            url=url_path,
            exchange_account_id=exchange_proposal_model.exchange_account_id,
            body=body
        )
        if not success:
            raise ErrorOnGetExchangeSimulationProposal()
        return exchange_simulation_proposal_data


if __name__ == '__main__':
    import asyncio

    async def abc():
        url = "https://sbxapi.ourinvest.com.br:43400/api/v1/produto/cambio/naturezaOperacao/4/taxa/BRL/USD/cliente/208785/spread/0.02"
        success, caronte_status, content = await ExchangeCompanyApi.request_as_client(method=AllowedHTTPMethods.GET, url=url, exchange_account_id=208785)
        print(content)
        print(content.get('token'))

    a = asyncio.run(abc())
