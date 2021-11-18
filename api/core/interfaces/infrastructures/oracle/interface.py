from abc import ABC, abstractmethod


class IInfrastructure(ABC):
    @staticmethod
    def get_connection(**kwargs):
        pass

    @classmethod
    @abstractmethod
    def get_singleton_connection(cls, **kwargs):
        pass
