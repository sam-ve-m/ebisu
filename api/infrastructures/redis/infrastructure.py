import aioredis

from api.core.interfaces.infrastructures.interface import IInfrastructure
from api.utils.env_config import config


class RedisInfrastructure(IInfrastructure):
    @staticmethod
    async def get_connection():
        redis = await aioredis.Redis(
            host=config("REDIS_HOST"),
            password=config("REDIS_PASSWORD"),
            db=15
        )
        return redis
