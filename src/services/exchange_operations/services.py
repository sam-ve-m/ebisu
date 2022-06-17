# EXTERNAL LIBS
from src.domain.model.exchange_operations.dto import ExchangeOperationsDtoBuilder
from src.domain.model.exchange_operations.model import ExchangeOperationsModel
from src.repositories.bank_account.repository import UserBankAccountRepository
from src.repositories.exchange_operations.repository import (
    UserExchangeOperationsRepository,
)


class ExchangeOperationsService:

    exchange_operations_repository_instance = UserExchangeOperationsRepository

    @classmethod
    async def get_service_response_to_save_exchange_operations(
        cls, jwt_data: dict, resume: dict
    ):

        name, cpf = await UserBankAccountRepository.get_cpf_and_name_from_user(
            unique_id=jwt_data.get("user").get("unique_id")
        )

        exchange_operations_dto = ExchangeOperationsDtoBuilder.build(
            jwt_data=jwt_data, resume=resume, name=name, cpf=cpf
        )

        exchange_model = ExchangeOperationsModel(
            exchange_operations_dto=exchange_operations_dto
        )
        exchange_data_was_dully_inserted = await cls.exchange_operations_repository_instance.save_user_exchange_operations(
            exchange_template=exchange_model.get_exchange_operations_template()
        )

        return exchange_data_was_dully_inserted
