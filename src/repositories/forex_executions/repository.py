# Ebisu
from src.domain.models.forex.proposal.execution_response_data.model import ExecutionResponseModel
from src.infrastructures.env_config import config
from src.repositories.base_repositories.mongo_db.base import MongoDbBaseRepository


class ProposalExecutionRepository(MongoDbBaseRepository):
    database = config("MONGODB_DATABASE_NAME")
    collection = config("MONGODB_PROPOSALS_EXECUTED")

    @classmethod
    async def insert_exchange_proposal(cls, execution_response_model: ExecutionResponseModel):
        data = execution_response_model.dict()
        result = await cls.insert(data=data)
        return result
