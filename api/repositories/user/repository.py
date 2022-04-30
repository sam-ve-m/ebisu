# OUTSIDE LIBRARIES

from api.infrastructures.env_config import config

from api.repositories.base_repositories.mongo_db.base import MongoDbBaseRepository


class UserRepository(MongoDbBaseRepository):

    database = config("MONGODB_DATABASE_NAME")
    collection = config("MONGODB_USER_COLLECTION")

    @classmethod
    async def get_user_portfolios(cls, unique_id: str):
        user_portfolios = await cls.find_one(query={"unique_id": unique_id}, project={"portfolios": True, "_id": False})
        return user_portfolios["portfolios"]
