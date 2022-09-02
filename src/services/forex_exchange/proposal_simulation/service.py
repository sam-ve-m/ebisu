from src.repositories.user.repository import UserRepository
from src.domain.validators.forex_exchange.currency_options import CurrencyExchange
from src.domain.models.proposal_simulation_exchange.model import ProposalSimulationModel

from caronte import OuroInvestApiTransport, AllowedHTTPMethods


class ProposalSimulationService:

    @staticmethod
    async def get_proposal_simulation(jwt_data: dict, currency_exchange: CurrencyExchange):
        unique_id = jwt_data.get("user", {}).get("unique_id")
        base = currency_exchange.base.value
        quote = currency_exchange.quote.value
        user_exchange_data = await UserRepository.get_user_exchange_data(unique_id=unique_id, base=base, quote=quote)
        if not user_exchange_data:
            raise UserDataNotFound
        proposal_simulation_model = ProposalSimulationModel(
            user_exchange_data=user_exchange_data,
            currency_exchange=currency_exchange)
        user_token = await ProposalSimulationService.get_user_token_on_route_21(
            proposal_simulation_model=proposal_simulation_model
        )
        pass

    @staticmethod
    async def get_user_token_on_route_21(proposal_simulation_model: ProposalSimulationModel):
        user_id = proposal_simulation_model.exchange_account_id
        url_path = await proposal_simulation_model.build_url_path_to_current_currency_quote()
        response_result = await OuroInvestApiTransport.request(method=AllowedHTTPMethods.GET, url=url_path, user_id=user_id)
        response_to_dict = await response_result.json()
        user_token = response_to_dict.get("token")
        if not user_token:
            raise NotFoundUserToken
        return user_token


    @staticmethod
    async def get_exchange_proposal_values_on_route_22():
        pass


if __name__ == '__main__':
    import asyncio

    async def abc():
        url = "https://sbxapi.ourinvest.com.br:43400/api/v1/produto/cambio/naturezaOperacao/4/taxa/BRL/USD/cliente/208785/spread/0.02"
        result = (await OuroInvestApiTransport.request(method=AllowedHTTPMethods.GET,
                                                    url=url,
                                                    user_id=208785
                                                )).json()

        print(result)
        print(result.get('token'))


    a = asyncio.run(abc())
