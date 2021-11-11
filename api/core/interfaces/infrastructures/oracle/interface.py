from abc import ABC, abstractmethod


class IOracle(ABC):

    @abstractmethod
    def execute(self, sql: str):
        pass

    @abstractmethod
    def get_one_data(self, sql: str):
        pass

    @abstractmethod
    def get_data(self, sql: str):
        pass