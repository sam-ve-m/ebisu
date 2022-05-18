from abc import ABC


class IInfrastructure(ABC):
    @staticmethod
    def get_connection(**kwargs):
        pass
