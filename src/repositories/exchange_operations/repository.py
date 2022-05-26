# STANDARD LIBS
import pytest

# EXTERNAL LIBS
from src.repositories.bank_account.repository import UserBankAccountRepository
from src.repositories.base_repositories.mongo_db.base import MongoDbBaseRepository
from tests.src.stubs.project_stubs.stub_data import payload_data_dummy

from src.infrastructures.env_config import config


class UserExchangeOperationsRepository(MongoDbBaseRepository):
    database = config("MONGODB_SNAPSHOT_DATABASE")
    collection = config("MONGODB_SNAPSHOT_COLLECTION")

    @classmethod
    async def save_user_exchange_operations(
            cls,
            jwt_data: dict,
            resume: dict):

        unique_id = jwt_data.get("unique_id")

        # Todo - find the user name as cpf according to the find_one at Mongo
        user_info_result = await UserBankAccountRepository.find_cpf_and_name_from_user(
            unique_id=unique_id
        )

        data_to_insert = {resume, user_info_result}

        # Todo - build the data to be sent to the database
        inserted_data = await cls.insert(data_to_insert)

#     date: datetime.now() # TEMOS
#     contract: str
#     ref_int: int
#     week: int
#     name: str
#     cpf: str
#     tp: TypeContract
#     valor_usd: float # TEMOS
#     taxa_cli: float  # TEMOS
#     valor_brl: float # TEMOS
#     date_brl: datetime # TEMOS
#     date_usd: datetime # TEMOS
#     du_brl: float
#     dc_usd: float
#     ajuste_brl: float
#     ajuste_usd: float
#     spot_client: float
#     brl_spot: float
#     zeramento: float
#     cdi: str  # %
#     linha: str  # %
#     brl_zer: float
#     pnl: float
#     spread: str  # % TEMOS

payload_data = {
    "exp": 1678209788,
    "created_at": 1646673788.442139,
    "scope": {
        "view_type": "default",
        "user_level": "client",
        "features": ["default", "realtime"],
    },
    "user": {
        "unique_id": "5952e960-219f-4161-bc26-908192e57d80",
        "nick_name": "RAST3",
        "portfolios": {
            "br": {"bovespa_account": "000000014-6", "bmf_account": "14"},
            "us": {"_": None},
        },
        "client_has_br_trade_allowed": False,
        "client_has_us_trade_allowed": False,
        "client_profile": "investor",
        "status": "SUCCESS",
    },
}

resume_obj = {
            "origin_account": "1234567",
            "account_destination": "98765432",
            "value": 1234.8,
            "cash_conversion": f"BRL>USD",
            "tax": 4.87,
            "spread": "2.98",
            "convert_value": 10234.0,
            "due_date": "20/09/1998",
        }

@pytest.mark.asyncio
async def test_when_registering_operations_on_database():
    response = await UserExchangeOperationsRepository.save_user_exchange_operations(
        jwt_data=payload_data, resume=resume_obj
    )
    print(response)
    return response