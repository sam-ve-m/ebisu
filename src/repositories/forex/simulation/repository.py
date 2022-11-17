# Ebisu
from src.domain.models.forex.proposal.simulation_response_data.model import SimulationResponseModel
from src.infrastructures.env_config import config
from src.repositories.base_repositories.mongo_db.base import MongoBaseRepository


class ExchangeSimulationRepository(MongoBaseRepository):
    database = config("MONGODB_DATABASE_EBISU")
    collection = config("MONGODB_PROPOSALS_SIMULATED")

    @classmethod
    async def insert_proposal(
        cls, simulation_response_model: SimulationResponseModel
    ):
        data = simulation_response_model.get_simulation_proposal_to_save_template()
        result = await cls.insert(data=data)
        return result
