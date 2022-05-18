#INTERNAL LIBS
from src.repositories.stock_portfolios.repository import StockPortfoliosRepository


class StockPortfoliosList:

    @classmethod
    async def get_stock_portfolios_response(cls, jwt_data: dict, portfolios_repository=StockPortfoliosRepository):
        thebes_answer = jwt_data.get("x-thebes-answer")
        unique_id = thebes_answer["user"]["unique_id"]

        stock_portfolios_response = await portfolios_repository.get_stock_portfolios_accounts(
            unique_id=unique_id
        )

        return stock_portfolios_response
