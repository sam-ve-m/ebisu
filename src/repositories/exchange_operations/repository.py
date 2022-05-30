# EXTERNAL LIBS
from src.repositories.base_repositories.mongo_db.base import MongoDbBaseRepository
from src.infrastructures.env_config import config


class UserExchangeOperationsRepository(MongoDbBaseRepository):
    database = config("MONGODB_SNAPSHOT_DATABASE")
    collection = config("MONGODB_SNAPSHOT_COLLECTION")

    @classmethod
    async def save_user_exchange_operations(
            cls,
            exchange_template: dict) -> bool:

        exchange_data_was_dully_inserted = await cls.insert(exchange_template)

        return exchange_data_was_dully_inserted
