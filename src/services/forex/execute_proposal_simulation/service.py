# Ebisu
from src.domain.exceptions.repository.forex.model import (
    CustomerPersonalDataNotFound,
    ErrorTryingToInsertData,
    ErrorTryingToGetForexAccountNumber,
    ErrorTryingToGetForexAccountData,
)
from src.domain.exceptions.service.forex.model import InsufficientFunds, ErrorTryingToLockResource, ErrorTryingToUnlock, \
    ErrorTryingToGetUniqueId

from src.domain.models.forex.balance.model import AllowedWithdraw
from src.domain.models.forex.proposal.execution_request_data.model import ExecutionModel
from src.domain.models.forex.proposal.execution_response_data.model import (
    ExecutionResponseModel,
)
from src.domain.request.forex.execution_proposal import ForexExecution
from src.repositories.user.repository import UserRepository
from src.repositories.forex_balance.repository import ForexBalanceRepository
from src.repositories.forex_executions.repository import ProposalExecutionRepository
from src.services.forex.jwt_exchange.service import JwtForexService
from src.services.forex.response_map.service import ForexResponseMap
from src.transport.forex.bifrost.transport import BifrostTransport

# Third party
from caronte import ExchangeCompanyApi, AllowedHTTPMethods
from etria_logger import Gladsheim
from halberd import BalanceLockManagerService, Resource


class ExecutionExchangeService:
    @classmethod
    async def execute_exchange_proposal(
        cls, payload: ForexExecution, jwt_data: dict
    ) -> True:
        token_decoded = await JwtForexService.decode(
            jwt_token=payload.proposal_simulation_token
        )
        forex_account = await cls.__get_forex_account(jwt_data=jwt_data)
        execution_model = ExecutionModel(
            jwt_data=jwt_data,
            token_decoded=token_decoded,
            payload=payload,
            forex_account=forex_account,
        )
        await cls.check_customer_has_enough_balance(execution_model=execution_model)
        content = await cls.execute_proposal_on_route_23(
            execution_model=execution_model
        )

        await BifrostTransport.build_template_and_send(execution_model=execution_model)
        execution_response_model = ExecutionResponseModel.get_model(
            execution_response=content, unique_id=execution_model.jwt.unique_id
        )
        await cls.__insert_execution_response_data(
            execution_response_model=execution_response_model
        )
        return True

    @classmethod
    async def check_customer_has_enough_balance(cls, execution_model: ExecutionModel):
        allowed_to_withdraw = None
        resource = Resource(
            unique_id=execution_model.jwt.unique_id,
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
                execution_model=execution_model.__dict__
            )
            raise ex
        finally:
            await cls.__unlock_balance(lock=lock)

    @classmethod
    async def execute_proposal_on_route_23(
        cls, execution_model: ExecutionModel
    ) -> dict:
        customer_name = await cls.__get_customer_name(execution_model=execution_model)
        body = execution_model.get_execute_proposal_body(customer_data=customer_name)
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
    async def __unlock_balance(lock) -> True:
        if not lock:
            return True
        success, unlock_status = await BalanceLockManagerService.unlock_balance(
            lock=lock
        )
        if not success:
            raise ErrorTryingToUnlock()
        return True

    @staticmethod
    async def __get_customer_name(execution_model: ExecutionModel) -> dict:
        unique_id = execution_model.jwt.unique_id
        name = await UserRepository.get_customer_name(unique_id=unique_id)
        if not name:
            raise CustomerPersonalDataNotFound()
        return name

    @staticmethod
    async def __insert_execution_response_data(
        execution_response_model: ExecutionResponseModel,
    ):
        result = await ProposalExecutionRepository.insert_exchange_proposal(
            execution_response_model=execution_response_model
        )
        if not result:
            raise ErrorTryingToInsertData()
        return True

    @staticmethod
    async def __get_forex_account(jwt_data: dict) -> int:
        unique_id = jwt_data.get("user", {}).get("unique_id")
        if not unique_id:
            raise ErrorTryingToGetUniqueId()
        forex_account_data = await UserRepository.get_forex_account_data(
            unique_id=unique_id
        )
        if not forex_account_data:
            raise ErrorTryingToGetForexAccountData()
        forex_account_number = (
            forex_account_data.get("ouro_invest", {})
            .get("account", {})
            .get("account_number")
        )
        if not forex_account_number:
            raise ErrorTryingToGetForexAccountNumber()
        return int(forex_account_number)
