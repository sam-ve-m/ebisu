# OUTSIDE LIBRARIES

from src.infrastructures.env_config import config

from src.repositories.base_repositories.mongo_db.base import MongoDbBaseRepository


class UserExchangeRepository(MongoDbBaseRepository):

    database = config("MONGODB_SNAPSHOT_DATABASE")
    collection = config("MONGODB_EXCHANGE_COLLECTION")

    @classmethod
    async def get_user_exchange_data(cls, exchange_account_id: int, base: str, quote: str) -> dict:
        user_exchange_data = await cls.find_one(
            query={"exchange_account_id": exchange_account_id, "base": base, "quote": quote}
        )

        if not user_exchange_data:
            user_exchange_data = {
                "exchange_account_id": exchange_account_id,
                "base": base,
                "quote": quote,
                "spread": config("SPREAD_DEFAULT")
            }

        return user_exchange_data
