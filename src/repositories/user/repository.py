# OUTSIDE LIBRARIES

from src.infrastructures.env_config import config

from src.repositories.base_repositories.mongo_db.base import MongoDbBaseRepository


class UserRepository(MongoDbBaseRepository):

    database = config("MONGODB_DATABASE_NAME")
    collection = config("MONGODB_USER_COLLECTION")

    @classmethod
    async def get_user_portfolios(cls, unique_id: str):
        user_portfolios = await cls.find_one(
            query={"unique_id": unique_id}, project={"portfolios": True, "_id": False}
        )
        return user_portfolios["portfolios"]

    @classmethod
    async def get_user_account_creation_date(cls, unique_id: str):
        user_data = await cls.find_one(
            query={"unique_id": unique_id}
        )

        creation_date = user_data.get("created_at")

        return creation_date
