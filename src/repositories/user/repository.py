# EXTERNAL LIBS
from src.infrastructures.env_config import config
from src.repositories.base_repositories.mongo_db.base import MongoDbBaseRepository


class UserRepository(MongoDbBaseRepository):
    database = config("MONGODB_DATABASE_NAME")
    collection = config("MONGODB_USER_COLLECTION")

    @classmethod
    async def get_nick_name(cls, unique_id: str):
        nick_name_data = await cls.find_one(
            query={"unique_id": unique_id},
            project={"nick_name": 1, '_id': 0}
        )
        return nick_name_data
