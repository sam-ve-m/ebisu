import pickle
from hashlib import sha1

from api.core.interfaces.infrastructures.cache.interface import ICache
from api.infrastructures.cache.infrastructure import RedisInfrastructure
from decouple import config


class RedisRepository(ICache):

    def __init__(self):
        self.infra = self.get_infrastructure()

    def get_infrastructure(self):
        infra = RedisInfrastructure()
        return infra.get_connection(
            host=config("CACHE_REDIS_HOST"),
            port=config("CACHE_REDIS_PORT"),
            db=config("CACHE_REDIS_DB"),
            password=config("CACHE_REDIS_PASSWORD"),
        )

    def get_or_create_cache(
            self, function_name: str, callback: callable, callback_kwargs: dict, ttl: int
    ):
        key = self.get_cache_key(
            function_name=function_name, callback_kwargs=callback_kwargs
        )
        cached_value = self.infra.get(key)
        if cached_value:
            return pickle.loads(cached_value)
        value_to_cache = callback(**callback_kwargs)
        self.infra.set(key, pickle.dumps(value_to_cache), ttl)
        return value_to_cache

    @staticmethod
    def get_cache_key(function_name: str, callback_kwargs: dict):
        _sha1 = sha1()
        _sha1.update(str(callback_kwargs).encode())
        cache_key = _sha1.hexdigest()
        return f"{function_name}:{cache_key}"