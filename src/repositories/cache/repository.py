# STANDARD LIBS
import pickle
from typing import Union, Optional

from src.core.interfaces.repositories.cache.interface import ICacheRepository
from src.infrastructures.redis.infraestructure import RedisInfrastructure
from src.infrastructures.env_config import config


class CacheRepository(ICacheRepository, RedisInfrastructure):
    prefix = "ebisu:"
    host = config("REDIS_HOST_URL")
    db = config("REDIS_CACHE_DB")

    @classmethod
    async def set(cls, key: str, value: dict, ttl: int = 0) -> None:
        redis = cls.get_redis()
        """ttl in secounds"""
        key = f"{cls.prefix}{key}"
        if ttl > 0:
            await redis.set(name=key, value=pickle.dumps(value), ex=ttl)
        else:
            await redis.set(name=key, value=pickle.dumps(value))

    @classmethod
    async def delete(cls, key: str):
        redis = cls.get_redis()
        redis.delete(key)
        return

    @classmethod
    async def get(cls, key: str) -> Union[dict, str, bytes]:
        redis = cls.get_redis()
        key = f"{cls.prefix}{key}"
        value = await redis.get(name=key)
        return value and pickle.loads(value) or value

    @classmethod
    async def get_keys(cls, pattern: str) -> Optional[list]:
        redis = cls.get_redis()
        return await redis.keys(pattern=pattern)

    @classmethod
    async def add_to_queue(cls, key: str, value: tuple) -> bool:
        redis = cls.get_redis()
        return await redis.rpush(key, pickle.dumps(value))

    @classmethod
    async def get_from_queue(cls, key: str) -> Optional[dict]:
        redis = cls.get_redis()
        value = await redis.lpop(name=key)
        return value and pickle.loads(value) or value
