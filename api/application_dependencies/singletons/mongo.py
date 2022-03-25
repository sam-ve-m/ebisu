from api.infrastructures.mongo.infrastructure import MongoInfrastructure
from api.repositories.mongo.repository import MongoRepository
from api.utils.env_config import config
from etria_logger import Gladsheim


class MongoSingletonInstance:
    mongo_singleton_instance = None

    @classmethod
    async def get_mongo_singleton_instance(cls):
        if cls.mongo_singleton_instance is None:
            try:
                infra = await MongoInfrastructure.get_connection()
                cls.mongo_singleton_instance = MongoRepository(
                    infra,
                    config("MONGO_DATABASE_POSEIDON"),
                    config("MONGO_COLLECTION_IZANAMI")
                )
            except Exception as exception:
                Gladsheim.error(
                    message=
                    f"""MongoSingletonInstance::get_mongo_singleton_instance:: 
                    Error connection with MongoDB, {exception}""",
                    error=exception,
                    )
        return cls.mongo_singleton_instance
