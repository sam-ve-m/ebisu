# Ebisu
from src.domain.models.forex.proposal.execution_response_data.model import (
    ExecutionResponseModel,
)
from src.infrastructures.env_config import config
from src.repositories.base_repositories.mongo_db.base import MongoBaseRepository


class ExchangeExecutionRepository(MongoBaseRepository):
    database = config("MONGODB_DATABASE_EBISU")
    collection = config("MONGODB_PROPOSALS_EXECUTED")

    @classmethod
    async def insert_exchange_proposal_executed(
        cls, execution_response_model: ExecutionResponseModel
    ):
        data = execution_response_model.get_execution_template_to_save()
        result = await cls.insert(data=data)
        return result
