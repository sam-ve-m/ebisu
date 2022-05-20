#INTERNAL LIBS
from src.domain.validators.stock_portfolios.validators import StockPortfoliosModel
from src.repositories.stock_portfolios.repository import StockPortfoliosRepository


class StockPortfoliosList:

    @classmethod
    async def get_all_stock_portfolios_list(cls,
                                            unique_id: str,
                                            portfolios_repository: StockPortfoliosRepository,
                                            **kwargs):

        stock_portfolios_response = await portfolios_repository.get_all_portfolios_list(
            unique_id=unique_id
        )
        return stock_portfolios_response

    @classmethod
    async def get_portfolios_by_type_of_classification(cls,
                                                    portfolios_repository: StockPortfoliosRepository,
                                                    unique_id: str,
                                                    portfolios_list = StockPortfoliosModel,
                                                    **kwargs
                                                    ):

        portfolio_classification = portfolios_list.portfolio_classification.value
        stock_portfolios_response = await portfolios_repository.get_portfolios_by_type(
            unique_id=unique_id,
            portfolio_classification=portfolio_classification
        )
        return stock_portfolios_response

    @classmethod
    async def get_portfolios_by_region_br_or_us(cls,
                                                portfolios_repository: StockPortfoliosRepository,
                                                unique_id: str,
                                                portfolios_list = StockPortfoliosModel,
                                                **kwargs):

        portfolios_region = portfolios_list.region.value

        stock_portfolios_response = await portfolios_repository.get_portfolios_by_region(
            unique_id=unique_id,
            region=portfolios_region
        )
        return stock_portfolios_response

    @classmethod
    async def get_portfolios_by_type_classification_and_region(cls,
                                                               portfolios_repository: StockPortfoliosRepository,
                                                               unique_id: str,
                                                               portfolios_list = StockPortfoliosModel,
                                                               **kwargs):

        portfolios_region = portfolios_list.region.value
        portfolio_classification = portfolios_list.portfolio_classification.value

        stock_portfolios_response = await portfolios_repository.get_portfolios_by_type_and_region(
            unique_id=unique_id,
            region=portfolios_region,
            portfolio_classification=portfolio_classification
        )
        return stock_portfolios_response

    @classmethod
    async def get_stock_portfolios_response(cls,
                                            jwt_data: dict,
                                            portfolios_list = StockPortfoliosModel,
                                            portfolios_repository=StockPortfoliosRepository):

        thebes_answer = jwt_data.get("x-thebes-answer")
        unique_id = thebes_answer["user"]["unique_id"]

        map_requisition_body = {
            (False, False): StockPortfoliosList.get_all_stock_portfolios_list,
            (True, False): StockPortfoliosList.get_portfolios_by_region_br_or_us,
            (False, True): StockPortfoliosList.get_portfolios_by_type_of_classification,
            (True, True): StockPortfoliosList.get_portfolios_by_type_classification_and_region,
        }

        map_key = \
            map_requisition_body.get((bool(portfolios_list.region), bool(portfolios_list.portfolio_classification)))

        map_response = await map_key(
                portfolios_list=portfolios_list,
                portfolios_repository=portfolios_repository,
                unique_id=unique_id)

        return map_response
