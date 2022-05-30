# EXTERNAL LIBS
from src.domain.validators.exchange_operations.validators import ExchangeOperationsModel
from src.repositories.bank_account.repository import UserBankAccountRepository
from src.repositories.exchange_operations.repository import UserExchangeOperationsRepository


class ExchangeOperationsService:

    exchange_operations_repository_instance = UserExchangeOperationsRepository

    @classmethod
    async def get_service_response_to_insert_exchange_operations_data_on_database(
            cls, jwt_data: dict, resume: dict):
        user = jwt_data.get("user")
        unique_id = user.get("unique_id")

        name, cpf = await UserBankAccountRepository.get_cpf_and_name_from_user(
            unique_id=unique_id
        )

        value = resume.get("value")
        cash_convertion = resume.get("cash_convertion")
        spread = resume.get("spread")
        tax = resume.get("tax")
        convert_value = resume.get("convert_value")
        due_date = resume.get("due_date")

        exchange_model = ExchangeOperationsModel(
                name=name,
                cpf=cpf,
                unique_id=unique_id,
                value=value,
                cash_convertion=cash_convertion,
                spread=spread,
                tax=tax,
                convert_value=convert_value,
                due_date=due_date
        )

        exchange_template = exchange_model.get_exchange_operations_template()

        exchange_data_was_dully_inserted = await cls.exchange_operations_repository_instance.save_user_exchange_operations(
            exchange_template=exchange_template
        )

        if not exchange_data_was_dully_inserted:
            exchange_response = {
                "Message": "MongoDBError:The data was not inserted!"
            }
            return exchange_response
