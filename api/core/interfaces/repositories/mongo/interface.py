from typing import Optional
from abc import ABC, abstractmethod
from pymongo.cursor import Cursor


class IMongo(ABC):
    @abstractmethod
    def insert(self, data: dict) -> bool:
        pass

    @abstractmethod
    def insert_many(self, data: list) -> bool:
        pass

    @abstractmethod
    def find_one(self, query: dict) -> Optional[dict]:
        pass

    @abstractmethod
    def find_all(self, query: dict) -> Optional[Cursor]:
        pass

    @abstractmethod
    def delete_one(self, query: dict) -> Optional[dict]:
        pass

    @abstractmethod
    def delete(self, query: dict) -> Optional[dict]:
        pass