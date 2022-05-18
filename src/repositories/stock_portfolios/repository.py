# EXTERNAL LIBS
from src.infrastructures.env_config import config
from src.repositories.base_repositories.mongo_db.base import MongoDbBaseRepository


class StockPortfoliosRepository(MongoDbBaseRepository):
    database = config("MONGODB_DATABASE_NAME")
    collection = config("MONGODB_USER_COLLECTION")

    # TODO - FILTER THE PORTFOLIO BY THE ACTIVE OR INACTIVE STATUS

    @classmethod
    async def get_stock_portfolios_accounts(cls, unique_id: str):

        stock_portfolios_response = await cls.find_one(
            query={"unique_id": unique_id},
            project={
                "portfolios": 1, "_id": 0
            }
        )

        if stock_portfolios_response is None:

            response = {"stock_portfolios": []}
            return response

        default_portfolios = stock_portfolios_response.get("portfolios").get("default")
        vnc_portfolios = stock_portfolios_response.get("portfolios").get("vnc")

        stock_portfolios = {
            "default": default_portfolios,
            "vnc_portfolios": vnc_portfolios
        }

        return stock_portfolios
