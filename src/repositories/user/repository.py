# EXTERNAL LIBS
from src.infrastructures.env_config import config
from src.repositories.base_repositories.mongo_db.base import MongoBaseRepository


class UserRepository(MongoBaseRepository):
    database = config("MONGODB_DATABASE_NAME")
    collection = config("MONGODB_USER_COLLECTION")

    @classmethod
    async def get_customer_name(cls, unique_id: str) -> dict:
        name = await cls.find_one(
            query={"unique_id": unique_id}, project={"name": 1, "_id": 0}
        )
        return name

    @classmethod
    async def get_forex_account_data(cls, unique_id: str) -> dict:
        forex_account_data = await cls.find_one(
            query={"unique_id": unique_id}, project={"ouro_invest.account": 1, "_id": 0}
        )
        return forex_account_data

    @classmethod
    async def get_user_portfolios(cls, unique_id: str):
        user_portfolios = await cls.find_one(
            query={"unique_id": unique_id}, project={"portfolios": True, "_id": False}
        )
        return user_portfolios.get("portfolios")
