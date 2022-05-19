#INTERNAL LIBS
from src.domain.validators.stock_portfolios.validators import StockPortfoliosModel
from src.repositories.stock_portfolios.repository import StockPortfoliosRepository


class StockPortfoliosList:

    @classmethod
    async def get_stock_portfolios_response(cls,
                                            jwt_data: dict,
                                            portfolios_list = StockPortfoliosModel,
                                            portfolios_repository=StockPortfoliosRepository):

        thebes_answer = jwt_data.get("x-thebes-answer")
        unique_id = thebes_answer["user"]["unique_id"]

        if not portfolios_list.region:

            if not portfolios_list.portfolio_classification:
                stock_portfolios_response = await portfolios_repository.get_all_portfolios_list(
                    unique_id=unique_id
                )
                return stock_portfolios_response

            portfolio_classification = portfolios_list.portfolio_classification.value
            stock_portfolios_response = await portfolios_repository.get_portfolios_by_type(
                unique_id=unique_id,
                portfolio_classification=portfolio_classification
            )
            return stock_portfolios_response

        if not portfolios_list.portfolio_classification:

            portfolios_region = portfolios_list.region.value

            stock_portfolios_response = await portfolios_repository.get_portfolios_by_region(
                unique_id=unique_id,
                region=portfolios_region
            )
            return stock_portfolios_response

        portfolios_region = portfolios_list.region.value
        portfolio_classification = portfolios_list.portfolio_classification.value

        stock_portfolios_response = await portfolios_repository.get_portfolios_by_type_and_region(
            unique_id=unique_id,
            region=portfolios_region,
            portfolio_classification=portfolio_classification
        )
        return stock_portfolios_response
