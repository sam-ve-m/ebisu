from abc import ABC, abstractmethod


class IInfrastructure(ABC):
    @staticmethod
    @abstractmethod
    def get_connection():
        pass
