# EXTERNAL LIBS
from src.domain.user_bank_account.status.enum import UserBankAccountStatus
from src.infrastructures.env_config import config
from src.repositories.base_repositories.mongo_db.base import MongoDbBaseRepository
from src.domain.models.database.bank_account import BankAccountModel


class UserBankAccountRepository(MongoDbBaseRepository):
    database = config("MONGODB_DATABASE_NAME")
    collection = config("MONGODB_USER_COLLECTION")

    @classmethod
    async def get_registered_user_bank_accounts(cls, unique_id: str) -> dict:
        user_bank_accounts_by_unique_id = await cls.find_one(
            query={"unique_id": unique_id},
            project={
                "_id": 0,
                "bank_accounts": {
                    "$filter": {
                        "input": "$bank_accounts",
                        "as": "item",
                        "cond": {"$eq": ["$$item.status", "active"]},
                    }
                },
            },
        )
        bank_accounts_result = user_bank_accounts_by_unique_id["bank_accounts"]
        user_bank_accounts_response = [
            BankAccountModel(**symbol)
            for symbol in bank_accounts_result
        ]
        return user_bank_accounts_response

    @classmethod
    async def save_registered_user_bank_accounts(
        cls, unique_id: str, bank_account: dict
    ) -> bool:
        user_bank_account_was_added = await cls.add_one_in_array(
            old={"unique_id": unique_id},
            new={"bank_accounts": bank_account},
            upsert=True,
        )
        return user_bank_account_was_added

    @classmethod
    async def existing_user_bank_account_and_is_activated(
        cls, unique_id: str, bank_account: dict
    ) -> bool:
        user_bank_account = await cls.find_one(
            query={
                "unique_id": unique_id,
                "bank_accounts": {
                    "$elemMatch": {
                        "bank": bank_account["bank"],
                        "account_type": bank_account["account_type"],
                        "agency": bank_account["agency"],
                        "account_number": bank_account["account_number"],
                        "status": UserBankAccountStatus.ACTIVE.value,
                    }
                },
            }
        )
        has_user_bank_account = bool(user_bank_account)
        return has_user_bank_account

    @classmethod
    async def user_bank_account_id_exists(
        cls, unique_id: str, bank_account_id: str
    ) -> bool:
        user_bank_account = await cls.find_one(
            query={
                "unique_id": unique_id,
                "bank_accounts": {
                    "$elemMatch": {
                        "id": bank_account_id,
                        "status": UserBankAccountStatus.ACTIVE.value,
                    }
                },
            }
        )
        user_bank_account_id_exists = bool(user_bank_account)
        return user_bank_account_id_exists

    @classmethod
    async def get_user_bank_account_by_id(
        cls, unique_id: str, bank_account_id: str
    ) -> dict:
        user_bank_account = await cls.find_one(
            query={
                "unique_id": unique_id,
                "bank_accounts": {"$elemMatch": {"id": bank_account_id}},
            },
            project={
                "_id": 0,
                "bank_accounts": {
                    "$filter": {
                        "input": "$bank_accounts",
                        "as": "item",
                        "cond": {"$eq": ["$$item.id", bank_account_id]},
                    }
                },
            },
        )
        bank_account = user_bank_account["bank_accounts"].pop(0)
        bank_account.pop("id")
        bank_account.pop("status")
        return bank_account

    @classmethod
    async def update_registered_user_bank_accounts(
        cls, unique_id: str, bank_account: dict
    ):
        bank_account_id = bank_account["id"]

        user_bank_account_was_updated = await cls.update_one(
            old={
                "unique_id": unique_id,
                "bank_accounts": {"$elemMatch": {"id": bank_account_id}},
            },
            new={
                "bank_accounts.$.bank": bank_account["bank"],
                "bank_accounts.$.account_type": bank_account["account_type"],
                "bank_accounts.$.agency": bank_account["agency"],
                "bank_accounts.$.account_number": bank_account["account_number"],
                "bank_accounts.$.account_name": bank_account["account_name"],
            },
        )
        return user_bank_account_was_updated

    @classmethod
    async def delete_registered_user_bank_accounts(
        cls, unique_id: str, bank_account: dict
    ):
        bank_account_id = bank_account["id"]
        user_bank_account_was_soft_deleted = await cls.update_one(
            old={
                "unique_id": unique_id,
                "bank_accounts": {"$elemMatch": {"id": bank_account_id}},
            },
            new={
                "bank_accounts.$.status": UserBankAccountStatus.DISABLED.value,
            },
        )
        return user_bank_account_was_soft_deleted

    @classmethod
    async def get_cpf_and_name_from_user(cls, unique_id: str):

        user_account_details = await cls.find_one(
            query={"unique_id": unique_id},
            project={"name": 1, "identifier_document": 1},
        )

        name = user_account_details.get("name")
        cpf = user_account_details.get("identifier_document").get("cpf")

        return name, cpf
