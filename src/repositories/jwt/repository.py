# OUTSIDE LIBRARIES
from src.infrastructures.env_config import config
from src.repositories.base_repositories.mongo_db.base import MongoDbBaseRepository


class JwtRepository(MongoDbBaseRepository):

    database = config("MONGODB_DATABASE_NAME")
    collection = config("MONGODB_JWT_COLLECTION")
