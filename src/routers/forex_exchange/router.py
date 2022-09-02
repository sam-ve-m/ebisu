from src.services.jwt.service_jwt import JwtService
from src.services.forex_exchange.proposal_simulation.service import ProposalSimulationService
from src.domain.validators.forex_exchange.currency_options import CurrencyExchange

from fastapi import Request, APIRouter, Depends


class ForexExchange:

    __forex_exchange_router = APIRouter(prefix="forex_exchange", tags=["Forex exchange"])

    @staticmethod
    def get_forex_exchange_router():
        return ForexExchange.__forex_exchange_router

    @staticmethod
    @__forex_exchange_router.get("/currency_exchange_simulation")
    async def get_exchange_simulation_proposal(
            request: Request, currency_exchange: CurrencyExchange
    ):
        jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
        result = await ProposalSimulationService.get_proposal_simulation(
            jwt_data=jwt_data,
            currency_exchange=currency_exchange
        )
        pass
