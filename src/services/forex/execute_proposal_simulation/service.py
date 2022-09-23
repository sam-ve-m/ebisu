from src.domain.validators.forex.execution_proposal import ForexExecution
from src.domain.models.forex.forex_proposal.execution.model import ExecutionProposalModel
from src.services.forex.jwt_ouroinvest.service import JwtService
from caronte import ExchangeCompanyApi
from halberd import (
    BalanceLockManagerService,
    Resource,
    Country as HalberdCountry,
    LockBalanceStatus
)


class ExecutionExchangeService:

    @classmethod
    async def execute_exchange_proposal(cls, payload: ForexExecution, jwt_data: dict):
        token_decoded = await JwtService.decode_jwt_token(jwt_data=payload.customer_proposal_token)
        execution_proposal_model = ExecutionProposalModel(
            jwt_data=jwt_data,
            token_decoded=token_decoded,
            payload=payload
        )
        pass

    @classmethod
    async def check_customer_has_enough_balance(cls):
