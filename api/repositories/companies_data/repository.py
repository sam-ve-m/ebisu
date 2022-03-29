from typing import Optional
from pymongo.cursor import Cursor

from api.infrastructures.connections.mongo.infrastructure import MongoInfrastructure
from api.infrastructures.env_config import config
from api.core.interfaces.repositories.mongo.interface import IMongo


class CompanyInformationRepository(IMongo):

    database_name = config("MONGO_DATABASE_POSEIDON")
    collection_name = config("MONGO_COLLECTION_IZANAMI")
    collection_instance = None
    infra = MongoInfrastructure

    @classmethod
    async def _get_collection(cls):
        if cls.collection_instance is None:
            client = await cls.infra.get_connection()
            database = client[cls.database_name]
            cls.collection_instance = database[cls.collection_name]
        return cls.collection_instance

    @classmethod
    async def get_company_name(cls, symbol: str):
        name = await cls.find_one({'symbol': symbol}, {'name': 1, '_id': 0})
        if not name:
            return [{}]
        return name.get('name')

    @classmethod
    async def insert(cls, data: dict) -> bool:
        collection = await cls._get_collection()
        return await collection.insert_one(data)

    @classmethod
    async def insert_many(cls, data: list) -> bool:
        collection = await cls._get_collection()
        return await collection.insert_many(data, ordered=False)

    @classmethod
    async def find_one(cls, query: dict, select_fields_dict=None) -> Optional[dict]:
        collection = await cls._get_collection()
        data = await collection.find_one(query, select_fields_dict)
        return data

    @classmethod
    def find_all(cls, query: dict, select_fields_dict=None) -> Optional[Cursor]:
        collection = await cls._get_collection()
        data = collection.find(query, select_fields_dict)
        return data

    @classmethod
    async def delete(cls, query: dict) -> bool:
        collection = await cls._get_collection()
        data = await collection.delete_many(query)
        return data

    @classmethod
    async def delete_one(cls, query: dict) -> bool:
        collection = await cls._get_collection()
        data = await collection.delete_one(query)
        return data
