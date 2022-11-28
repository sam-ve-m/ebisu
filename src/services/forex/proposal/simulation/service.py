# Ebisu
from typing import Union

from persephone_client import Persephone

from src.domain.enums.persephone import PersephoneQueue, PersephoneSchema
from src.domain.exceptions.domain.model.forex.model import ErrorValidatingSimulationProposalData
from src.domain.exceptions.repository.forex.model import CustomerForexDataNotFound
from src.domain.exceptions.service.forex.model import (
    InconsistentResultInRoute21,
    InconsistentResultInRoute22,
)
from src.domain.exceptions.service.auditing_trail.model import FailToSaveAuditingTrail
from src.domain.exceptions.service.forex.model import CustomerQuotationTokenNotFound, ErrorTryingToGetUniqueId
from src.domain.models.device_info.dto import DeviceInfo
from src.domain.models.forex.proposal.simulation_request_data.model import (
    SimulationModel,
)
from src.domain.models.forex.proposal.simulation_response_data.model import (
    SimulationResponseModel,
)
from src.domain.models.thebes_answer.model import ThebesAnswer
from src.domain.request.forex.currency_options import CurrencyExchange
from src.domain.validators.forex.proposal.simulation.validator import (
    ContentRoute21,
    ContentRoute22,
)
from src.infrastructures.env_config import config
from src.repositories.user_exchange.repository import UserExchangeRepository
from src.repositories.forex.simulation.repository import ExchangeSimulationRepository
from src.services.forex.account.service import ForexAccount
from src.services.forex.response_mapping.service import ForexResponseMap

# Third party
from caronte import AllowedHTTPMethods, ExchangeCompanyApi
from etria_logger import Gladsheim


class ForexSimulation:
    @classmethod
    async def get_proposal_simulation(
        cls, jwt_data: dict, payload: CurrencyExchange,
            device_info: DeviceInfo
    ) -> dict:
        unique_id = ThebesAnswer(jwt_data=jwt_data).unique_id
        client_id = await ForexAccount.get_client_id(unique_id=unique_id)
        account_number = await ForexAccount.get_account_number(unique_id=unique_id)
        customer_exchange_data = await cls.__get_customer_spread_by_operation_type(
            account_number=account_number, payload=payload
        )
        simulation_model = SimulationModel(
            customer_exchange_data=customer_exchange_data,
            payload=payload,
            client_id=client_id,
        )
        content_21 = await cls.__get_customer_token_on_route_21(
            simulation_model=simulation_model
        )
        content_21_validated = await cls.__validate_route_21_result_content(
            content=content_21
        )
        content_22 = await cls.__get_exchange_simulation_proposal_data_on_route_22(
            customer_token=content_21_validated.token,
            simulation_model=simulation_model,
        )
        
        content_22_validated = await cls.__validate_route_22_result_content(
            content=content_22
        )

        await cls.__log_in_persephone_to_audit(
            exchange_simulation_proposal_data=content_22,
            device_info=device_info,
            unique_id=unique_id,
        )

        simulation_response_model = SimulationResponseModel(
            content_21_validated=content_21_validated,
            content_22_validated=content_22_validated,
            unique_id=unique_id,
        )
        await ExchangeSimulationRepository.insert_proposal(
            simulation_response_model=simulation_response_model
        )
        simulation_proposal_template = (
            simulation_response_model.get_simulation_proposal_template()
        )
        return simulation_proposal_template

    @staticmethod
    def __get_unique_id(jwt_data: dict) -> str:
        unique_id = jwt_data.get("user", {}).get("unique_id")
        if not unique_id:
            raise ErrorTryingToGetUniqueId()
        return unique_id

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
    async def __log_in_persephone_to_audit(
        exchange_simulation_proposal_data: dict,
        device_info: DeviceInfo,
        unique_id: str
    ):
        (
            sent_to_persephone,
            status_sent_to_persephone,
        ) = await Persephone.send_to_persephone(
            topic=config("PERSEPHONE_TOPIC_MONEY_MOVEMENT_EXCHANGE"),
            partition=PersephoneQueue.EXCHANGE_PROPOSAL_SIMULATION.value,
            message={
                "unique_id": unique_id,
                "device_id": device_info.device_id,
                "device_info": device_info.decrypted_device_info,
                "proposal_data": exchange_simulation_proposal_data,
            },
            schema_name=PersephoneSchema.EXCHANGE_PROPOSAL_SIMULATION.value,
        )
        if sent_to_persephone is False:
            raise FailToSaveAuditingTrail("common.process_issue")

    @staticmethod
    async def __get_customer_spread_by_operation_type(
        account_number: int, payload: CurrencyExchange
    ) -> dict:
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
        content_21 = await ForexResponseMap.get_response(
            caronte_response=caronte_response
        )
        return content_21

    @staticmethod
    async def __get_exchange_simulation_proposal_data_on_route_22(
        customer_token: str,
        simulation_model: SimulationModel,
    ) -> dict:
        url_path = await simulation_model.get_url_path_to_request_exchange_simulation()
        body = await simulation_model.get_body_template_to_request_exchange_simulation(
            customer_token=customer_token
        )
        Gladsheim.debug(message="Calling route 22", body=body)
        caronte_response = await ExchangeCompanyApi.request_as_client(
            method=AllowedHTTPMethods.GET,
            url=url_path,
            exchange_account_id=simulation_model.client_id,
            body=body,
        )
        content_22 = await ForexResponseMap.get_response(
            caronte_response=caronte_response
        )
        return content_22

    @staticmethod
    async def __validate_route_21_result_content(
        content: dict,
    ) -> ContentRoute21:
        try:
            content_validated = ContentRoute21(**content)
            return content_validated
        except Exception as ex:
            Gladsheim.info(message=(str(ex)))
            raise InconsistentResultInRoute21()

    @staticmethod
    async def __validate_route_22_result_content(
        content: dict,
    ) -> ContentRoute22:
        try:
            content_22_validated = ContentRoute22(**content)
            return content_22_validated
        except Exception as ex:
            Gladsheim.info(message=(str(ex)))
            raise InconsistentResultInRoute22()
