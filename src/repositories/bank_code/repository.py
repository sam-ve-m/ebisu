from src.repositories.base_repositories.oracle.repository import OracleBaseRepository
from src.infrastructures.env_config import config


class BankCodeRepository(OracleBaseRepository):

    service = config("ORACLE_BASE_SERVICE_BR")
    user = config("ORACLE_BASE_USER")
    password = config("ORACLE_BASE_PASSWORD")
    base_dns = config("ORACLE_BASE_DSN")
    port = config("ORACLE_BASE_PORT")

    @classmethod
    def get_bank_code_from_database(cls, bank: str) -> str:

        query = f"""
                SELECT CD_BANCO FROM CORRWIN.TSCBANCO WHERE CD_BANCO = ('{bank}')
                """

        bank_code_result = cls.get_data(sql=query)

        return bank_code_result

    @classmethod
    def get_all_bank_codes_from_database(cls):

        query = f"""SELECT CD_BANCO, NM_BANCO FROM CORRWIN.TSCBANCO"""

        bank_code_result = cls.get_data(sql=query)

        return bank_code_result
