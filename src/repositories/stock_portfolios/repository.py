# EXTERNAL LIBS
from src.infrastructures.env_config import config
from src.repositories.base_repositories.mongo_db.base import MongoDbBaseRepository


class StockPortfoliosRepository(MongoDbBaseRepository):
    database = config("MONGODB_DATABASE_NAME")
    collection = config("MONGODB_USER_COLLECTION")

    # TODO - FILTER PORTFOLIO BY THE ACTIVE OR INACTIVE STATUS

    @classmethod
    async def get_all_portfolios_list(cls, unique_id: str):

        stock_portfolios_response = await cls.find_one(
            query={"unique_id": unique_id},
            project={
                "portfolios": 1, "_id": 0
            }
        )

        default_portfolios = stock_portfolios_response.get("portfolios").get("default")
        vnc_portfolios = stock_portfolios_response.get("portfolios").get("vnc")

        if stock_portfolios_response is None:
            response = {
                "default": {},
                "vnc_portfolios": {}
            }
            return response

        stock_portfolios = {
            "default": default_portfolios,
            "vnc_portfolios": vnc_portfolios
        }

        return stock_portfolios

    @classmethod
    async def get_portfolios_by_region(cls, unique_id: str, region: str):
        region_portfolios = region.lower()

        stock_portfolios_response = await cls.find_one(
            query={"unique_id": unique_id},
            project={
                f"portfolios.vnc.{region_portfolios}": 1,
                f"portfolios.default.{region_portfolios}": 1,
                "_id": 0
            }
        )

        if stock_portfolios_response is None:
            response = {
                "default": {},
                "vnc_portfolios": {}
            }
            return response

        default_portfolios = stock_portfolios_response.get("portfolios").get("default")
        vnc_portfolios = stock_portfolios_response.get("portfolios").get("vnc")

        stock_portfolios_response = {
            "default": default_portfolios,
            "vnc_portfolios": vnc_portfolios
        }

        return stock_portfolios_response

    @classmethod
    async def get_portfolios_by_type(cls, unique_id: str, portfolio_classification: str):
        classification_type = portfolio_classification.lower()

        stock_portfolios_response = await cls.find_one(
            query={"unique_id": unique_id},
            project={
                f"portfolios.{classification_type}": 1,
                "_id": 0
            }
        )

        if stock_portfolios_response is None:
            response = {
                f"{classification_type}": {}
            }
            return response

        portfolio_result = stock_portfolios_response.get("portfolios").get(f"{classification_type}")

        stock_portfolios_response = {
            f"{classification_type}": portfolio_result,
        }

        return stock_portfolios_response

    @classmethod
    async def get_portfolios_by_type_and_region(cls, unique_id: str, portfolio_classification: str, region: str):
        classification_type = portfolio_classification.lower()
        region_portfolios = region.lower()

        stock_portfolios_response = await cls.find_one(
            query={"unique_id": unique_id},
            project={
                f"portfolios.{classification_type}": 1,
                f"{region_portfolios}": 1,
                "_id": 0
            }
        )

        if stock_portfolios_response is None:
            response = {
                f"{classification_type}": {}
            }
            return response

        portfolio_result = \
            stock_portfolios_response.get("portfolios").get(f"{classification_type}").get(f"{region_portfolios}")

        stock_portfolios_response = {
            f"{region_portfolios}": portfolio_result,
        }

        return stock_portfolios_response
