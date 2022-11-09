# Ebisu
from src.domain.exceptions.domain.model.forex.model import ErrorValidatingSimulationProposalData
from src.domain.exceptions.repository.forex.model import CustomerForexDataNotFound
from src.domain.exceptions.service.forex.model import CustomerQuotationTokenNotFound
from src.domain.models.forex.proposal.simulation_request_data.model import (
    SimulationModel,
)
from src.domain.models.forex.proposal.simulation_response_data.model import (
    SimulationResponseModel,
)
from src.domain.request.forex.currency_options import CurrencyExchange
from src.repositories.user_exchange.repository import UserExchangeRepository
from src.services.forex.account.service import ForexAccount
from src.services.forex.response_mapping.service import ForexResponseMap

# Standards
from typing import Union

# Third party
from caronte import AllowedHTTPMethods, ExchangeCompanyApi
from etria_logger import Gladsheim


class ForexSimulation:
    @classmethod
    async def get_proposal_simulation(
        cls, jwt_data: dict, payload: CurrencyExchange
    ) -> dict:
        client_id = await ForexAccount.get_client_id(jwt_data=jwt_data)
        account_number = await ForexAccount.get_account_number(jwt_data=jwt_data)
        customer_exchange_data = await cls.__get_customer_spread_by_operation_type(
            account_number=account_number, payload=payload
        )
        simulation_model = SimulationModel(
            customer_exchange_data=customer_exchange_data,
            payload=payload,
            client_id=client_id,
        )
        content = await cls.__get_customer_token_on_route_21(
            simulation_model=simulation_model
        )
        customer_token = await cls.__validate_if_token_exists_in_content(
            content=content
        )
        exchange_simulation_proposal_data = (
            await cls.__get_exchange_simulation_proposal_data_on_route_22(
                customer_token=customer_token,
                simulation_model=simulation_model,
            )
        )
        exchange_simulation_proposal_response = (
            await cls.__treatment_and_validation_exchange_simulation_data(
                exchange_simulation_proposal_data=exchange_simulation_proposal_data
            )
        )

        return exchange_simulation_proposal_response

    @staticmethod
    async def __treatment_and_validation_exchange_simulation_data(
        exchange_simulation_proposal_data: dict,
    ) -> Union[dict, ErrorValidatingSimulationProposalData]:
        try:
            exchange_simulation_model = (
                await SimulationResponseModel.get_customer_exchange_model(
                    exchange_simulation_proposal_data=exchange_simulation_proposal_data
                )
            )
            exchange_simulation_proposal_response = {
                "exchange_simulation_proposal": exchange_simulation_model.dict()
            }
            return exchange_simulation_proposal_response
        except Exception as ex:
            Gladsheim.error(error=ex)
            raise ErrorValidatingSimulationProposalData()

    @staticmethod
    async def __get_customer_spread_by_operation_type(
        account_number: int, payload: CurrencyExchange
    ) -> Union[dict, CustomerForexDataNotFound]:
        customer_exchange_data = await UserExchangeRepository.get_spread_data(
            account_number=account_number,
            base=payload.base,
            quote=payload.quote,
        )
        if not customer_exchange_data:
            raise CustomerForexDataNotFound()
        return customer_exchange_data

    @staticmethod
    async def __get_customer_token_on_route_21(
        simulation_model: SimulationModel,
    ) -> dict:
        url_path = (
            await simulation_model.build_url_path_to_request_current_currency_quote()
        )
        caronte_response = await ExchangeCompanyApi.request_as_client(
            method=AllowedHTTPMethods.GET,
            url=url_path,
            exchange_account_id=simulation_model.client_id,
        )
        customer_token = await ForexResponseMap.get_response(
            caronte_response=caronte_response
        )
        return customer_token

    @staticmethod
    async def __get_exchange_simulation_proposal_data_on_route_22(
        customer_token: str,
        simulation_model: SimulationModel,
    ) -> dict:
        url_path = await simulation_model.get_url_path_to_request_exchange_simulation()
        body = await simulation_model.get_body_template_to_request_exchange_simulation(
            customer_token=customer_token
        )
        caronte_response = await ExchangeCompanyApi.request_as_client(
            method=AllowedHTTPMethods.GET,
            url=url_path,
            exchange_account_id=simulation_model.client_id,
            body=body,
        )
        exchange_simulation_proposal_data = await ForexResponseMap.get_response(
            caronte_response=caronte_response
        )
        return exchange_simulation_proposal_data

    @staticmethod
    async def __validate_if_token_exists_in_content(
        content: dict,
    ) -> Union[str, CustomerQuotationTokenNotFound]:
        customer_token = content.get("token")
        if not customer_token:
            raise CustomerQuotationTokenNotFound()
        return customer_token
