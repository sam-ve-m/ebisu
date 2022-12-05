from src.repositories.base_repositories.oracle.repository import OracleBaseRepository


class BankCodeRepository(OracleBaseRepository):
    @classmethod
    def _get_connection(cls):
        return cls.infra.get_base_connection_br()

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
