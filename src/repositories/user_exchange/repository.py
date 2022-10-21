# Ebisu
from src.infrastructures.env_config import config
from src.repositories.base_repositories.mongo_db.base import MongoBaseRepository


class UserExchangeRepository(MongoBaseRepository):

    database = config("MONGODB_SNAPSHOT_DATABASE")
    collection = config("MONGODB_EXCHANGE_COLLECTION")

    @classmethod
    async def get_spread_data(
        cls, forex_account_number: int, base: str, quote: str
    ) -> dict:
        spread_data = await cls.find_one(
            query={"account_number": forex_account_number, "base": base, "quote": quote}
        )

        if not spread_data:
            spread_data = {
                "account_number": forex_account_number,
                "base": base,
                "quote": quote,
                "spread": config("SPREAD_DEFAULT"),
            }

        return spread_data
