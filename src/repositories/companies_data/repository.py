from src.infrastructures.env_config import config
from src.repositories.base_repositories.mongo_db.base import MongoBaseRepository


class CompanyInformationRepository(MongoBaseRepository):

    database = config("MONGO_DATABASE_POSEIDON")
    collection = config("MONGO_COLLECTION_IZANAMI")

    @classmethod
    async def get_company_name(cls, symbol: str):
        name = await cls.find_one(
            query={"symbol": symbol}, project={"name": 1, "_id": 0}
        )
        if not name:
            return None
        return name.get("name")
