
import motor.motor_asyncio as motor

from api.core.interfaces.infrastructures.interface import IInfrastructure
from api.utils.env_config import config


class MongoInfrastructure(IInfrastructure):

    @staticmethod
    async def get_connection():
        return motor.AsyncIOMotorClient(
            f'{config("MONGODB_CONNECTION")}://{config("MONGODB_USER")}:{config("MONGODB_PASSWORD")}@{config("MONGODB_HOST")}:{config("MONGODB_PORT")}'
        )
