from fastapi import Request, APIRouter, Depends


class ForexExchange:

    __forex_exchange_router = APIRouter(prefix="forex_exchange", tags=["Forex exchange"])

    @staticmethod
    def get_forex_exchange_router():
        return ForexExchange.__forex_exchange_router

    @staticmethod
    @__forex_exchange_router.get("/simulation_proposal")
    async def get_exchange_simulation_proposal(
            request: Request,
    ):
        pass
