# STANDARD LIBS
from fastapi import Request, APIRouter, Depends

from src.domain.validators.user_exchange_operations.exchange_operations_model import UserExchangeOperationsModel
from src.services.jwt.service_jwt import JwtService
from src.services.user_exchange_operations.service import CreateUserExchangeOperationsService


class UserExchangeOperationsRouter:

    __user_exchange_operations = APIRouter()

    @staticmethod
    def get_user_account_router():
        return UserExchangeOperationsRouter.__user_exchange_operations

    @staticmethod
    @__user_exchange_operations.post("/user_exchange_operations", tags=["User Exchange Operations"])
    async def create_user_exchange_operations(
        request: Request, create_exchange_operations: UserExchangeOperationsModel
    ):
        jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
        response_exchange_operations = (
            await CreateUserExchangeOperationsService.create_user_exchange_operations(jwt_data=jwt_data)
        )
        return response_exchange_operations