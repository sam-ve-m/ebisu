from abc import ABC, abstractmethod


class IInfrastructure(ABC):
    @staticmethod
    def get_connection(**kwargs):
        pass
