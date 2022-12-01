# Ebisu
from src.domain.exceptions.repository.forex.model import (
    CustomerPersonalDataNotFound,
    ErrorTryingToInsertData,
)
from src.domain.exceptions.service.forex.model import (
    InsufficientFunds,
    ErrorTryingToLockResource,
    ErrorTryingToUnlock,
    InconsistentResultInRoute23,
)
from src.domain.models.forex.balance.model import AllowedWithdraw
from src.domain.models.forex.proposal.execution_request_data.model import ExecutionModel
from src.domain.models.forex.proposal.execution_response_data.model import (
    ExecutionResponseModel,
)
from src.domain.models.thebes_answer.model import ThebesAnswer
from src.domain.request.forex.execution_proposal import ForexSimulationToken
from src.domain.validators.forex.proposal.execution.validator import ContentRoute23
from src.repositories.user.repository import UserRepository
from src.repositories.forex.balance.repository import ForexBalanceRepository
from src.repositories.forex.execution.repository import ExchangeExecutionRepository
from src.services.forex.account.service import ForexAccount
from src.services.forex.decrypt_token.service import DecryptService
from src.services.forex.response_mapping.service import ForexResponseMap
from src.transport.forex.bifrost.transport import BifrostTransport

# Standards
from typing import Union

# Third party
from caronte import ExchangeCompanyApi, AllowedHTTPMethods
from etria_logger import Gladsheim
from halberd import BalanceLockManagerService, Resource


class ForexExecution:
    @classmethod
    async def execute_proposal(
        cls, payload: ForexSimulationToken, jwt_data: dict
    ) -> True:
        token_decoded = await DecryptService.decode(
            jwt_token=payload.proposal_simulation_token
        )
        thebes_answer = ThebesAnswer(jwt_data=jwt_data)
        account_number = await ForexAccount.get_account_number(
            unique_id=thebes_answer.unique_id
        )
        execution_model = ExecutionModel(
            thebes_answer=thebes_answer,
            token_decoded=token_decoded,
            payload=payload,
            account_number=account_number,
        )
        await cls.check_customer_has_enough_balance(execution_model=execution_model)
        content = await cls.execute_proposal_on_route_23(
            execution_model=execution_model
        )
        content_validated = await cls.__validate_route_23_result_content(
            content=content
        )
        await BifrostTransport.build_template_and_send(execution_model=execution_model)
        execution_response_model = ExecutionResponseModel(
            unique_id=thebes_answer.unique_id,
            execution_model=execution_model,
            content_validated=content_validated,
        )
        await cls.__insert_execution_response_data(
            execution_response_model=execution_response_model
        )
        return True

    @classmethod
    async def check_customer_has_enough_balance(cls, execution_model: ExecutionModel):
        allowed_to_withdraw = None
        resource = Resource(
            unique_id=execution_model.thebes_answer.unique_id,
            country=execution_model.origin_country,
            account=execution_model.origin_account,
        )
        lock = await cls.__lock_balance(resource=resource)
        try:
            allowed_to_withdraw: AllowedWithdraw = (
                await ForexBalanceRepository.get_allowed_to_withdraw(
                    redis_hash=execution_model.redis_hash
                )
            )
            if not execution_model.exchange_proposal_value <= allowed_to_withdraw.total:
                raise InsufficientFunds()
        except Exception as ex:
            Gladsheim.error(
                error=ex,
                allowed_to_withdraw=allowed_to_withdraw,
                execution_model=execution_model.__dict__,
            )
            raise ex
        finally:
            await cls.__unlock_balance(lock=lock)

    @classmethod
    async def execute_proposal_on_route_23(
        cls, execution_model: ExecutionModel
    ) -> dict:
        customer_name = await cls.__get_customer_name(execution_model=execution_model)
        body = execution_model.get_execute_proposal_body(customer_name=customer_name)
        url = execution_model.get_execution_url()
        caronte_response = await ExchangeCompanyApi.request_as_client(
            exchange_account_id=execution_model.token_decoded.forex_account,
            method=AllowedHTTPMethods.POST,
            body=body,
            url=url,
        )
        content = await ForexResponseMap.get_response(caronte_response=caronte_response)
        return content

    @staticmethod
    async def __lock_balance(resource: Resource):
        success, status, lock = await BalanceLockManagerService.lock_balance(
            resource_to_lock=resource
        )
        if not success:
            raise ErrorTryingToLockResource()
        return lock

    @staticmethod
    async def __unlock_balance(lock) -> Union[bool, ErrorTryingToUnlock]:
        if not lock:
            return True
        success, unlock_status = await BalanceLockManagerService.unlock_balance(
            lock=lock
        )
        if not success:
            raise ErrorTryingToUnlock()
        return True

    @staticmethod
    async def __get_customer_name(
        execution_model: ExecutionModel,
    ) -> Union[dict, CustomerPersonalDataNotFound]:
        unique_id = execution_model.thebes_answer.unique_id
        name = await UserRepository.get_customer_name(unique_id=unique_id)
        if not name:
            raise CustomerPersonalDataNotFound()
        return name

    @staticmethod
    async def __insert_execution_response_data(
        execution_response_model: ExecutionResponseModel,
    ) -> Union[bool, ErrorTryingToInsertData]:
        result = await ExchangeExecutionRepository.insert_exchange_proposal_executed(
            execution_response_model=execution_response_model
        )
        if not result:
            raise ErrorTryingToInsertData()
        return True

    @staticmethod
    async def __validate_route_23_result_content(
        content: dict,
    ) -> ContentRoute23:
        try:
            content_validated = ContentRoute23(**content)
            return content_validated
        except Exception as ex:
            Gladsheim.info(message=(str(ex)))
            raise InconsistentResultInRoute23()
