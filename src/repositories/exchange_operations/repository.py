# STANDARD LIBS
from datetime import datetime
import pytest

# EXTERNAL LIBS
from src.repositories.bank_account.repository import UserBankAccountRepository
from src.repositories.base_repositories.mongo_db.base import MongoDbBaseRepository
from src.infrastructures.env_config import config


class UserExchangeOperationsRepository(MongoDbBaseRepository):
    database = config("MONGODB_SNAPSHOT_DATABASE")
    collection = config("MONGODB_SNAPSHOT_COLLECTION")

    @classmethod
    async def save_user_exchange_operations(
            cls,
            jwt_data: dict,
            resume: dict):

        user = jwt_data.get("user")
        unique_id = user.get("unique_id")

        user_info_result = await UserBankAccountRepository.get_cpf_and_name_from_user(
            unique_id=unique_id
        )

        extra_data = {
                "date": datetime.now(),
                "contract": "1111",
                "ref_int": 1234,
                "week": 20,
                "tp": "C",
                "du_brl": 4.5,
                "dc_usd": 5.5,
                "ajuste_brl": 1.4,
                "ajuste_usd": 2.5,
                "spot_client": 1.6,
                "brl_spot": 10.4,
                "zeramento": 10.4,
                "cdi": "20%",  # %
                "linha": "lalala",  # %
                "brl_zer": "30%",
                "pnl": 10.4
        }

        user_info_result.update(extra_data)
        user_info_result.update(resume)

        exchange_data_was_dully_inserted = await cls.insert(user_info_result)

        return exchange_data_was_dully_inserted
