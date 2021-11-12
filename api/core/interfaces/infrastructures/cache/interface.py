from abc import ABC, abstractmethod


class ICache(ABC):

    @staticmethod
    @abstractmethod
    def get_cache_key(function_name: str, callback_kwargs: dict) -> str:
        pass

    @abstractmethod
    def get_or_create_cache(self, function_name: str, callback: callable, callback_kwargs: dict, ttl: int):
        pass
