# EXTERNAL LIBS
from etria_logger import Gladsheim
from src.domain.validators.exchange_operations.validators import ExchangeOperationsModel
from src.repositories.bank_account.repository import UserBankAccountRepository
from src.repositories.exchange_operations.repository import UserExchangeOperationsRepository


class ExchangeOperationsService:

    exchange_operations_repository_instance = UserExchangeOperationsRepository

    @classmethod
    async def get_service_response_to_save_exchange_operations(
            cls, jwt_data: dict, resume: dict):
        user = jwt_data.get("user")
        unique_id = user.get("unique_id")

        name, cpf = await UserBankAccountRepository.get_cpf_and_name_from_user(
            unique_id=unique_id
        )

        value = resume.get("value")
        cash_conversion = resume.get("cash_conversion")
        spread = resume.get("spread")
        tax = resume.get("tax")
        convert_value = resume.get("convert_value")
        due_date = resume.get("due_date")

        exchange_model = ExchangeOperationsModel(
                name=name,
                cpf=cpf,
                unique_id=unique_id,
                value=value,
                cash_conversion=cash_conversion,
                spread=spread,
                tax=tax,
                convert_value=convert_value,
                due_date=due_date
        )

        exchange_template = exchange_model.get_exchange_operations_template()

        try:
            exchange_data_was_dully_inserted = \
                await cls.exchange_operations_repository_instance.save_user_exchange_operations(

                exchange_template=exchange_template
            )

            return exchange_data_was_dully_inserted

        except Exception as err:

            Gladsheim.error(
                message=f"MongoDB::save_user_exchange_operations:: Error on inserting the data, {err}",
                error=err,
            )
