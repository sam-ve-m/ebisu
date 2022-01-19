from typing import Optional
from pymongo.cursor import Cursor

from api.core.interfaces.repositories.mongo.interface import IMongo


class MongoRepository(IMongo):

    def __init__(self, infra, database, collection):
        self.infra = infra
        self.database = self.infra[database]
        self.collection = self.database[collection]

    async def insert(self, data: dict) -> bool:
        return await self.collection.insert_one(data)

    async def insert_many(self, data: list) -> bool:
        return await self.collection.insert_many(data, ordered=False)

    async def find_one(self, query: dict, select_fields_dict=None) -> Optional[dict]:
        data = await self.collection.find_one(query, select_fields_dict)
        return data

    def find_all(self, query: dict, select_fields_dict=None) -> Optional[Cursor]:
        data = self.collection.find(query, select_fields_dict)
        return data

    async def delete(self, query: dict) -> bool:
        data = await self.collection.delete_many(query)
        return data

    async def delete_one(self, query: dict) -> bool:
        data = await self.collection.delete_one(query)
        return data
