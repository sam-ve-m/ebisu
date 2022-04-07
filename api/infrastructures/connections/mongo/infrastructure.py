import motor.motor_asyncio as motor

from api.core.interfaces.infrastructures.interface import IInfrastructure
from api.infrastructures.env_config import config
from etria_logger import Gladsheim


class MongoInfrastructure(IInfrastructure):

    client = None

    @classmethod
    async def get_connection(cls):
        if cls.client is None:
            try:
                cls.client = motor.AsyncIOMotorClient(
                    f'{config("MONGODB_CONNECTION")}://{config("MONGODB_USER")}:{config("MONGODB_PASSWORD")}@'
                    f'{config("MONGODB_HOST")}:{config("MONGODB_PORT")}'
                )
            except Exception as exception:
                Gladsheim.error(
                    message=f"""MongoInfrastructure::get_connection::Error on connecting with Mongo: {exception}""",
                    error=exception,
                )

        return cls.client
