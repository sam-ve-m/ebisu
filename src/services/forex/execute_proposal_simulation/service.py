from src.domain.validators.forex.execution_proposal import ForexExecution
from src.services.forex.jwt.service import JwtService
from caronte import ExchangeCompanyApi

class ExecutionExchangeService:

    @classmethod
    async def execute_exchange_proposal(cls, payload: ForexExecution, jwt_data: dict):
        token_decoded = JwtService.decode_jwt_token(jwt_data=payload.customer_proposal_token)
        execution_proposal_model =
        pass