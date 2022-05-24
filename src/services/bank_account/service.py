# STANDARD LIBS
from uuid import uuid4

# INTERNAL LIBRARIES
from src.domain.user_bank_account.status.enum import UserBankAccountStatus
from src.exceptions.exceptions import BadRequestError, InternalServerError
from src.repositories.bank_account.repository import UserBankAccountRepository


class UserBankAccountService:
    @classmethod
    async def create_user_bank_accounts(
        cls, jwt_data: dict, bank_account_repository=UserBankAccountRepository
    ):
        thebes_answer = jwt_data["x-thebes-answer"]
        unique_id = thebes_answer["user"]["unique_id"]
        bank_account = jwt_data["bank_account"]

        bank_code_exists = (
            await bank_account_repository.bank_code_from_client_exists(
                bank_account=bank_account
            )
        )
        if not bank_code_exists:
            raise BadRequestError("bank_code.this_is_not_a_valid_bank_code")

        is_bank_account_from_user = (
            await bank_account_repository.is_user_bank_account_from_client(
                unique_id=unique_id, bank_account=bank_account
            )
        )
        if not is_bank_account_from_user:
            raise BadRequestError("user.bank_account_is_not_yours")

        bank_account_exists_and_is_activated = (
            await bank_account_repository.existing_user_bank_account_and_is_activated(
                unique_id=unique_id, bank_account=bank_account
            )
        )
        if bank_account_exists_and_is_activated:
            raise BadRequestError("common.register_exists")

        bank_account.update(
            {"id": uuid4(), "status": UserBankAccountStatus.ACTIVE.value}
        )
        if "cpf" in bank_account:
            del bank_account["cpf"]

        user_bank_account_was_added = (
            await UserBankAccountRepository.save_registered_user_bank_accounts(
                unique_id=unique_id, bank_account=bank_account
            )
        )

        if not user_bank_account_was_added:
            raise InternalServerError("common.process_issue")

        create_account_response = {
            "message": "Created",
        }

        return create_account_response

    @classmethod
    async def get_user_bank_accounts(
        cls, jwt_data: dict, bank_account_repository=UserBankAccountRepository
    ):
        thebes_answer = jwt_data.get("x-thebes-answer")
        unique_id = thebes_answer["user"]["unique_id"]
        bank_accounts = await bank_account_repository.get_registered_user_bank_accounts(
            unique_id=unique_id
        )
        if bank_accounts is None:
            bank_accounts = {"bank_accounts": []}
        return bank_accounts

    @classmethod
    async def update_user_bank_account(
        cls, jwt_data: dict, bank_account_repository=UserBankAccountRepository
    ):
        thebes_answer = jwt_data["x-thebes-answer"]
        unique_id = thebes_answer["user"]["unique_id"]
        bank_account = jwt_data["bank_account"]
        bank_account_id = bank_account["id"]

        user_bank_account_id_exists = (
            await bank_account_repository.user_bank_account_id_exists(
                unique_id=unique_id, bank_account_id=bank_account_id
            )
        )
        if not user_bank_account_id_exists:
            raise BadRequestError("common.register_not_exists")

        user_bank_account_was_updated = (
            await bank_account_repository.update_registered_user_bank_accounts(
                unique_id=unique_id, bank_account=bank_account
            )
        )
        if not user_bank_account_was_updated:
            raise InternalServerError("common.process_issue")

        bank_code_exists = (
            await bank_account_repository.bank_code_from_client_exists(
                bank_account=bank_account
            )
        )
        if not bank_code_exists:
            raise BadRequestError("bank_code.invalid_bank_code")

        update_bank_account_response = {
            "message": "Updated",
        }

        return update_bank_account_response

    @classmethod
    async def delete_user_bank_account(
        cls, jwt_data: dict, bank_account_repository=UserBankAccountRepository
    ):
        thebes_answer = jwt_data["x-thebes-answer"]
        unique_id = thebes_answer["user"]["unique_id"]
        bank_account = jwt_data["bank_account"]
        bank_account_id = bank_account["id"]
        user_bank_account_id_exists = (
            await bank_account_repository.user_bank_account_id_exists(
                unique_id=unique_id, bank_account_id=bank_account_id
            )
        )
        if not user_bank_account_id_exists:
            raise BadRequestError("common.register_not_exists")

        user_bank_account_was_soft_deleted = (
            await bank_account_repository.delete_registered_user_bank_accounts(
                unique_id=unique_id, bank_account=bank_account
            )
        )
        if not user_bank_account_was_soft_deleted:
            raise InternalServerError("common.process_issue")

        delete_bank_account_response = {
            "message": "Deleted",
        }

        return delete_bank_account_response
