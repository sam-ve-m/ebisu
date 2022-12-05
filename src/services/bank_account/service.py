import datetime
from uuid import uuid4

from fastapi.openapi.models import Response

from nidavellir import Sindri
from src.domain.enums.persephone import PersephoneSchema, PersephoneQueue
from src.domain.exceptions.service.bank_account.model import (
    BankAccountAlreadyExists,
    BankAccountNotExists,
)
from src.domain.exceptions.service.auditing_trail.model import FailToSaveAuditingTrail
from src.domain.exceptions.service.unexpected.internal_server_error.model import (
    InternalServerError,
)
from src.domain.models.device_info.dto import DeviceInfo
from src.domain.user_bank_account.status.enum import UserBankAccountStatus
from src.repositories.bank_account.repository import UserBankAccountRepository
from src.services.get_bank_code.service import GetBankCode
from persephone_client import Persephone
from src.infrastructures.env_config import config
from src.domain.models.response.create_bank_account.response_model import (
    ListBankAccountsResponse,
)
from src.domain.responses.http_response_model import ResponseModel
from src.domain.enums.response.internal_code import InternalCode
from http import HTTPStatus


class UserBankAccountService:
    @classmethod
    async def create_user_bank_accounts(
        cls,
        jwt_data: dict,
        device_info: DeviceInfo,
        bank_account_repository=UserBankAccountRepository,
    ) -> Response:
        thebes_answer = jwt_data["x-thebes-answer"]
        unique_id = thebes_answer["user"]["unique_id"]
        bank_account = jwt_data["bank_account"]

        bank_account_exists_and_is_activated = (
            await bank_account_repository.existing_user_bank_account_and_is_activated(
                unique_id=unique_id, bank_account=bank_account
            )
        )
        if bank_account_exists_and_is_activated:
            raise BankAccountAlreadyExists("common.register_exists")

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
                "device_id": device_info.device_id,
                "device_info": device_info.decrypted_device_info,
                "bank_account": bank_account,
                "_created_at": datetime.datetime.utcnow(),
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

        result = ResponseModel(
            success=True,
            internal_code=InternalCode.SUCCESS,
            message="Created",
        ).build_http_response(status_code=HTTPStatus.OK)

        return result

    @classmethod
    async def get_user_bank_accounts(
        cls, jwt_data: dict, bank_account_repository=UserBankAccountRepository
    ) -> Response:
        thebes_answer = jwt_data.get("x-thebes-answer")
        unique_id = thebes_answer["user"]["unique_id"]
        bank_accounts_from_database = (
            await bank_account_repository.get_registered_user_bank_accounts(
                unique_id=unique_id
            )
        )
        response_model = ListBankAccountsResponse.to_response(
            models=bank_accounts_from_database
        )
        user_bank_accounts_result = response_model.dict()
        Sindri.dict_to_primitive_types(user_bank_accounts_result)
        return user_bank_accounts_result

    @classmethod
    async def update_user_bank_account(
        cls,
        jwt_data: dict,
        device_info: DeviceInfo,
        bank_account_repository=UserBankAccountRepository,
    ) -> Response:
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
            raise BankAccountNotExists()

        (
            sent_to_persephone,
            status_sent_to_persephone,
        ) = await Persephone.send_to_persephone(
            topic=config("PERSEPHONE_TOPIC_CLIENT_BANK_ACCOUNT"),
            partition=PersephoneQueue.UPDATE_BANK_ACCOUNT.value,
            message={
                "unique_id": unique_id,
                "device_id": device_info.device_id,
                "device_info": device_info.decrypted_device_info,
                "bank_account": bank_account,
                "_created_at": datetime.datetime.utcnow(),
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

        result = ResponseModel(
            success=True,
            internal_code=InternalCode.SUCCESS,
            message="Updated",
        ).build_http_response(status_code=HTTPStatus.OK)

        return result

    @classmethod
    async def delete_user_bank_account(
        cls,
        jwt_data: dict,
        device_info: DeviceInfo,
        bank_account_repository=UserBankAccountRepository,
    ) -> Response:
        thebes_answer = jwt_data["x-thebes-answer"]
        unique_id = thebes_answer["user"]["unique_id"]
        bank_account = jwt_data["bank_account"]

        user_bank_account_id_exists = (
            await bank_account_repository.user_bank_account_id_exists(
                unique_id=unique_id, bank_account_id=bank_account["id"]
            )
        )
        if not user_bank_account_id_exists:
            raise BankAccountNotExists()

        (
            sent_to_persephone,
            status_sent_to_persephone,
        ) = await Persephone.send_to_persephone(
            topic=config("PERSEPHONE_TOPIC_CLIENT_BANK_ACCOUNT"),
            partition=PersephoneQueue.DELETE_BANK_ACCOUNT.value,
            message={
                "unique_id": unique_id,
                "device_id": device_info.device_id,
                "device_info": device_info.decrypted_device_info,
                "bank_account": bank_account,
                "_created_at": datetime.datetime.utcnow(),
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

        result = ResponseModel(
            success=True,
            internal_code=InternalCode.SUCCESS,
            message="Deleted",
        ).build_http_response(status_code=HTTPStatus.OK)

        return result

    @classmethod
    def bank_code_from_client_exists(cls, bank: str) -> bool:
        bank_code_result = GetBankCode.get_bank_code_from_database(bank=bank)
        return bool(bank_code_result)
