from api.infrastructures.mongo.infrastructure import MongoInfrastructure
from api.repositories.mongo.repository import MongoRepository
from api.utils.env_config import config


class MongoSingletonInstance:
    mongo_singleton_instance = None

    @classmethod
    async def get_mongo_singleton_instance(cls):
        if cls.mongo_singleton_instance is None:
            infra = await MongoInfrastructure.get_connection()
            cls.mongo_singleton_instance = MongoRepository(infra, config("MONGO_DATABASE_POSEIDON"),
                                                           config("MONGO_COLLECTION_IZANAMI"))

        return cls.mongo_singleton_instance
