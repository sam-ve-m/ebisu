from abc import ABC


class IOracleInfrastructure(ABC):
    @staticmethod
    def get_connection(**kwargs):
        pass
