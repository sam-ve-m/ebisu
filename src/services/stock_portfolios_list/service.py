# INTERNAL LIBS
from src.domain.validators.stock_portfolios.validators import UserPortfoliosModel
from src.repositories.user_portfolios.repository import UserPortfoliosRepository


class UserPortfoliosList:
    @classmethod
    async def get_all_stock_portfolios_list(
        cls, unique_id: str, portfolios_repository: UserPortfoliosRepository, **kwargs
    ):

        stock_portfolios_response = await portfolios_repository.get_all_portfolios_list(
            unique_id=unique_id
        )
        return stock_portfolios_response

    @classmethod
    async def get_portfolios_by_type_of_classification(
        cls,
        portfolios_repository: UserPortfoliosRepository,
        unique_id: str,
        user_portfolios=UserPortfoliosModel,
        **kwargs
    ):

        portfolio_classification = user_portfolios.portfolio_classification.value
        stock_portfolios_response = await portfolios_repository.get_portfolios_by_type(
            unique_id=unique_id, portfolio_classification=portfolio_classification
        )
        return stock_portfolios_response

    @classmethod
    async def get_portfolios_by_region_br_or_us(
        cls,
        portfolios_repository: UserPortfoliosRepository,
        unique_id: str,
        user_portfolios=UserPortfoliosModel,
        **kwargs
    ):

        portfolios_region = user_portfolios.region.value

        stock_portfolios_response = (
            await portfolios_repository.get_portfolios_by_region(
                unique_id=unique_id, region=portfolios_region
            )
        )
        return stock_portfolios_response

    @classmethod
    async def get_portfolios_by_type_classification_and_region(
        cls,
        portfolios_repository: UserPortfoliosRepository,
        unique_id: str,
        user_portfolios=UserPortfoliosModel,
        **kwargs
    ):

        portfolios_region = user_portfolios.region.value
        portfolio_classification = user_portfolios.portfolio_classification.value

        stock_portfolios_response = (
            await portfolios_repository.get_portfolios_by_type_and_region(
                unique_id=unique_id,
                region=portfolios_region,
                portfolio_classification=portfolio_classification,
            )
        )
        return stock_portfolios_response

    @classmethod
    async def get_user_portfolios_response(
        cls,
        jwt_data: dict,
        user_portfolios=UserPortfoliosModel,
        portfolios_repository=UserPortfoliosRepository,
    ):

        thebes_answer = jwt_data.get("x-thebes-answer")
        unique_id = thebes_answer["user"]["unique_id"]

        map_requisition_body = {
            (False, False): UserPortfoliosList.get_all_stock_portfolios_list,
            (True, False): UserPortfoliosList.get_portfolios_by_region_br_or_us,
            (False, True): UserPortfoliosList.get_portfolios_by_type_of_classification,
            (True, True): UserPortfoliosList.get_portfolios_by_type_classification_and_region,
        }

        map_key = map_requisition_body.get(
            (
                bool(user_portfolios.region),
                bool(user_portfolios.portfolio_classification),
            )
        )

        map_response = await map_key(
            user_portfolios=user_portfolios,
            portfolios_repository=portfolios_repository,
            unique_id=unique_id,
        )

        return map_response
