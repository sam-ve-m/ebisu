# Ebisu
from src.domain.exceptions.domain.forex_exchange.exception import (
    ErrorOnValidateExchangeSimulationProposalData,
)
from src.domain.exceptions.repository.exception import CustomerExchangeDataNotFound
from src.domain.exceptions.service.forex_exchange.exception import (
    CustomerQuotationTokenNotFound,
)
from src.domain.models.forex_exchange.customer_exchange_request_data.model import (
    CustomerExchangeRequestModel,
)
from src.domain.models.forex_exchange.customer_exchange_response_data.model import (
    CustomerExchangeResponseModel,
)
from src.domain.validators.forex_exchange.currency_options import CurrencyExchange
from src.repositories.user.repository import UserRepository
from src.services.forex_exchange.response_exchange_map.service import (
    ExchangeResponseMap,
)

# Standards
from typing import Union

# Third party
from caronte import AllowedHTTPMethods, ExchangeCompanyApi
from etria_logger import Gladsheim


class CustomerExchangeService:
    @classmethod
    async def get_proposal_simulation(
        cls, jwt_data: dict, currency_exchange: CurrencyExchange
    ) -> dict:
        exchange_account_id = jwt_data.get("user", {}).get(
            "exchange_account_id", 208785
        )
        customer_exchange_data = await cls.__get_customer_exchange_account_data(
            exchange_account_id=exchange_account_id, payload=currency_exchange
        )
        customer_exchange_request_model = CustomerExchangeRequestModel(
            customer_exchange_data=customer_exchange_data,
            payload=currency_exchange,
            exchange_account_id=exchange_account_id,
        )
        content = await cls.__get_customer_token_on_route_21(
            customer_exchange_request_model=customer_exchange_request_model
        )
        customer_token = await cls.__validate_if_token_exists_in_content(
            content=content
        )
        exchange_simulation_proposal_data = (
            await cls.__get_exchange_simulation_proposal_data_on_route_22(
                customer_token=customer_token,
                customer_exchange_request_model=customer_exchange_request_model,
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
    ) -> dict:
        try:
            exchange_simulation_model = (
                await CustomerExchangeResponseModel.get_customer_exchange_model(
                    exchange_simulation_proposal_data=exchange_simulation_proposal_data
                )
            )
            exchange_simulation_proposal_response = {
                "exchange_simulation_proposal": exchange_simulation_model.dict()
            }
            return exchange_simulation_proposal_response
        except Exception as ex:
            Gladsheim.error(error=ex)
            raise ErrorOnValidateExchangeSimulationProposalData()

    @staticmethod
    async def __get_customer_exchange_account_data(
        exchange_account_id: int, payload: CurrencyExchange
    ) -> Union[CustomerExchangeDataNotFound, dict]:
        customer_exchange_data = await UserRepository.get_user_exchange_data(
            exchange_account_id=exchange_account_id,
            base=payload.base,
            quote=payload.quote,
        )
        if not customer_exchange_data:
            raise CustomerExchangeDataNotFound()
        return customer_exchange_data

    @staticmethod
    async def __get_customer_token_on_route_21(
        customer_exchange_request_model: CustomerExchangeRequestModel,
    ) -> dict:
        url_path = (
            await customer_exchange_request_model.build_url_path_to_request_current_currency_quote()
        )
        caronte_response = await ExchangeCompanyApi.request_as_client(
            method=AllowedHTTPMethods.GET,
            url=url_path,
            exchange_account_id=customer_exchange_request_model.exchange_account_id,
        )
        customer_token = await ExchangeResponseMap.get_response(
            caronte_response=caronte_response
        )
        return customer_token

    @staticmethod
    async def __get_exchange_simulation_proposal_data_on_route_22(
        customer_token: str,
        customer_exchange_request_model: CustomerExchangeRequestModel,
    ) -> dict:
        url_path = (
            await customer_exchange_request_model.get_url_path_to_request_exchange_simulation()
        )
        body = await customer_exchange_request_model.get_body_template_to_request_exchange_simulation(
            customer_token=customer_token
        )
        caronte_response = await ExchangeCompanyApi.request_as_client(
            method=AllowedHTTPMethods.GET,
            url=url_path,
            exchange_account_id=customer_exchange_request_model.exchange_account_id,
            body=body,
        )
        exchange_simulation_proposal_data = await ExchangeResponseMap.get_response(
            caronte_response=caronte_response
        )
        return exchange_simulation_proposal_data

    @staticmethod
    async def __validate_if_token_exists_in_content(content: dict) -> str:
        customer_token = content.get("token")
        if not customer_token:
            raise CustomerQuotationTokenNotFound()
        return customer_token
