# Ebisu
from src.domain.exceptions.repository.forex.exception import CustomerPersonalDataNotFound
from src.domain.exceptions.service.forex.exception import (
    ErrorTryingToLockResource, ErrorTryingToUnlock, InsufficientFunds
)
from src.domain.models.forex.balance.model import AllowedWithdraw
from src.domain.models.forex.proposal.execution.model import ExecutionProposalModel
from src.domain.validators.forex.execution_proposal import ForexExecution
from src.repositories.user.repository import UserRepository
from src.repositories.forex_balance.repository import ForexBalanceRepository
from src.services.forex.jwt_ouroinvest.service import JwtOuroInvestService

# Third party
from caronte import ExchangeCompanyApi, AllowedHTTPMethods, CaronteStatusResponse
from halberd import (
    BalanceLockManagerService,
    Resource
)


class ExecutionExchangeService:

    @classmethod
    async def execute_exchange_proposal(cls, payload: ForexExecution, jwt_data: dict):
        token_decoded = await JwtOuroInvestService.decode_jwt_token(jwt_data=payload.customer_proposal_token)
        execution_proposal_model = ExecutionProposalModel(
            jwt_data=jwt_data,
            token_decoded=token_decoded,
            payload=payload
        )
        await cls.check_customer_has_enough_balance(execution_proposal_model=execution_proposal_model)
        pass

    @classmethod
    async def check_customer_has_enough_balance(cls, execution_proposal_model: ExecutionProposalModel):
        exchange_proposal_value = execution_proposal_model.token_decoded.net_value
        resource = Resource(
            unique_id=execution_proposal_model.jwt.unique_id,
            country=execution_proposal_model.origin_country.lower(),
            account=execution_proposal_model.origin_account.lower()
        )
        lock = await cls.__lock_balance(resource=resource)
        allowed_to_withdraw: AllowedWithdraw = await ForexBalanceRepository.get_allowed_to_withdraw(
            redis_hash=execution_proposal_model.redis_hash
        )
        await cls.__unlock_balance(lock=lock)
        if not exchange_proposal_value <= allowed_to_withdraw.total:
            raise InsufficientFunds
        return True

    @staticmethod
    async def execute_proposal_on_route_23(execution_proposal_model: ExecutionProposalModel):
        body = execution_proposal_model.get_execute_proposal_body()
        await ExchangeCompanyApi.request_as_client(
            exchange_account_id=execution_proposal_model.token_decoded.forex_account,
            method=AllowedHTTPMethods.POST,
            body=body
        )

    @staticmethod
    async def __lock_balance(resource: Resource):
        success, status, lock = await BalanceLockManagerService.lock_balance(
            resource_to_lock=resource
        )
        if not success:
            raise ErrorTryingToLockResource()
        return lock

    @staticmethod
    async def __unlock_balance(lock):
        if not lock:
            return True
        success, unlock_status = await BalanceLockManagerService.unlock_balance(lock=lock)
        if not success:
            raise ErrorTryingToUnlock()
        return True

    @staticmethod
    async def __get_customer_name(execution_proposal_model: ExecutionProposalModel):
        unique_id = execution_proposal_model.jwt.unique_id
        name = await UserRepository.get_customer_name(unique_id=unique_id)
        if not name:
            raise CustomerPersonalDataNotFound()
        return name
