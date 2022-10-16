# Ebisu
from src.infrastructures.env_config import config
from src.repositories.base_repositories.mongo_db.base import MongoDbBaseRepository


class UserExchangeRepository(MongoDbBaseRepository):

    database = config("MONGODB_SNAPSHOT_DATABASE")
    collection = config("MONGODB_EXCHANGE_COLLECTION")

    @classmethod
    async def get_spread_data(
        cls, account_number: int, base: str, quote: str
    ) -> dict:
        spread_data = await cls.find_one(
            query={"account_number": account_number, "base": base, "quote": quote}
        )

        if not spread_data:
            spread_data = {
                "account_number": account_number,
                "base": base,
                "quote": quote,
                "spread": config("SPREAD_DEFAULT"),
            }

        return spread_data
