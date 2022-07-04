# STANDARD LIBS
import datetime
from uuid import uuid4

# INTERNAL LIBRARIES
from src.domain.enums.persephone import PersephoneSchema, PersephoneQueue
from src.domain.exception import FailToSaveAuditingTrail
from src.domain.user_bank_account.status.enum import UserBankAccountStatus
from src.exceptions.exceptions import BadRequestError, InternalServerError
from src.repositories.bank_account.repository import UserBankAccountRepository
from src.services.get_bank_code.service import GetBankCode
from persephone_client import Persephone
from src.infrastructures.env_config import config


class UserBankAccountService:
    @classmethod
    async def create_user_bank_accounts(
        cls, jwt_data: dict, bank_account_repository=UserBankAccountRepository
    ):
        thebes_answer = jwt_data["x-thebes-answer"]
        unique_id = thebes_answer["user"]["unique_id"]
        bank_account = jwt_data["bank_account"]
        device_info = bank_account.pop("device_info")

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

        (
            sent_to_persephone,
            status_sent_to_persephone,
        ) = await Persephone.send_to_persephone(
            topic=config("PERSEPHONE_TOPIC_CLIENT_BANK_ACCOUNT"),
            partition=PersephoneQueue.REGISTER_BANK_ACCOUNT.value,
            message={
                "unique_id": unique_id,
                "device_info": device_info,
                "bank_account": bank_account,
                "_created_at": datetime.datetime.utcnow()
            },
            schema_name=PersephoneSchema.REGISTER_CLIENT_BANK_ACCOUNT.value,
        )
        if sent_to_persephone is False:
            raise FailToSaveAuditingTrail("common.process_issue")

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
        device_info = bank_account.pop("device_info")

        user_bank_account_id_exists = (
            await bank_account_repository.user_bank_account_id_exists(
                unique_id=unique_id, bank_account_id=bank_account_id
            )
        )
        if not user_bank_account_id_exists:
            raise BadRequestError("common.register_not_exists")

        (
            sent_to_persephone,
            status_sent_to_persephone,
        ) = await Persephone.send_to_persephone(
            topic=config("PERSEPHONE_TOPIC_CLIENT_BANK_ACCOUNT"),
            partition=PersephoneQueue.UPDATE_BANK_ACCOUNT.value,
            message={
                "unique_id": unique_id,
                "device_info": device_info,
                "bank_account": bank_account,
                "_created_at": datetime.datetime.utcnow()
            },
            schema_name=PersephoneSchema.UPDATE_CLIENT_BANK_ACCOUNT.value,
        )
        if sent_to_persephone is False:
            raise FailToSaveAuditingTrail()

        user_bank_account_was_updated = (
            await bank_account_repository.update_registered_user_bank_accounts(
                unique_id=unique_id, bank_account=bank_account
            )
        )
        if not user_bank_account_was_updated:
            raise InternalServerError("common.process_issue")

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
        device_info = bank_account.pop("device_info")

        user_bank_account_id_exists = (
            await bank_account_repository.user_bank_account_id_exists(
                unique_id=unique_id, bank_account_id=bank_account["id"]
            )
        )
        if not user_bank_account_id_exists:
            raise BadRequestError("common.register_not_exists")

        (
            sent_to_persephone,
            status_sent_to_persephone,
        ) = await Persephone.send_to_persephone(
            topic=config("PERSEPHONE_TOPIC_CLIENT_BANK_ACCOUNT"),
            partition=PersephoneQueue.DELETE_BANK_ACCOUNT.value,
            message={
                "unique_id": unique_id,
                "device_info": device_info,
                "bank_account": bank_account,
                "_created_at": datetime.datetime.utcnow()
            },
            schema_name=PersephoneSchema.DELETE_CLIENT_BANK_ACCOUNT.value,
        )
        if sent_to_persephone is False:
            raise FailToSaveAuditingTrail("common.process_issue")

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

    @classmethod
    def bank_code_from_client_exists(cls, bank: str) -> bool:
        bank_code_result = GetBankCode.get_bank_code_from_database(bank=bank)

        return bool(bank_code_result)
