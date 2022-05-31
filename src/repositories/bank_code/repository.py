from src.repositories.base_repositories.oracle.repository import OracleBaseRepository
from src.infrastructures.env_config import config


class BankCodeRepository(OracleBaseRepository):

    service = config("ORACLE_SERVICE_STATEMENT")
    user = config("ORACLE_USER_STATEMENT")
    password = config("ORACLE_PASSWORD_STATEMENT")
    base_dns = config("ORACLE_BASE_DSN_STATEMENT")
    port = config("ORACLE_PORT_STATEMENT")

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
