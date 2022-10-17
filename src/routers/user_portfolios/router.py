# STANDARD LIBS
from fastapi import Request, APIRouter, Depends

from src.services.stock_portfolios_list.service import UserPortfoliosList
from src.domain.request.stock_portfolios.validators import UserPortfoliosModel
from src.services.jwt.service import JwtService


class UserPortfoliosRouter:

    __user_portfolios_router = APIRouter()

    @staticmethod
    def get_user_portfolios_router():
        return UserPortfoliosRouter.__user_portfolios_router

    @staticmethod
    @__user_portfolios_router.get("/user_portfolios_list", tags=["Stock Portfolio"])
    async def user_portfolios_list(
        request: Request, user_portfolios: UserPortfoliosModel = Depends()
    ):
        jwt_data = await JwtService.validate_and_decode_thebes_answer(request=request)
        jwt_data = {"x-thebes-answer": jwt_data}
        response = await UserPortfoliosList.get_user_portfolios_response(
            jwt_data, user_portfolios=user_portfolios
        )
        return response
