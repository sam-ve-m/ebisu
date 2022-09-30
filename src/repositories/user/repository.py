# EXTERNAL LIBS
from src.infrastructures.env_config import config
from src.repositories.base_repositories.mongo_db.base import MongoDbBaseRepository


class UserRepository(MongoDbBaseRepository):
    database = config("MONGODB_DATABASE_NAME")
    collection = config("MONGODB_USER_COLLECTION")

    @classmethod
    async def get_customer_name(cls, unique_id: str) -> dict:
        name = await cls.find_one(
            query={"unique_id": unique_id},
            project={"name": 1, '_id': 0}
        )
        return name

    @classmethod
    async def get_forex_account(cls, unique_id: str) -> dict:
        forex_account_number = await cls.find_one(
            query={"unique_id": unique_id},
            project={"account_number": 1, '_id': 0}
        )
        return forex_account_number
