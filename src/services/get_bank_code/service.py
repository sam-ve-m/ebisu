from src.repositories.statements.repository import StatementsRepository


class GetBankCode:

    oracle_singleton_instance = StatementsRepository

    @classmethod
    def normalize_bank_code(cls, bank_code_list: dict) -> dict:
        normalize_data = {
            "code": bank_code_list.get("CD_BANCO"),
            "description": bank_code_list.get("NM_BANCO"),
        }
        return normalize_data

    @classmethod
    def get_service_response(cls):

        query = f"""SELECT CD_BANCO, NM_BANCO FROM CORRWIN.TSCBANCO"""

        bank_code_result = cls.oracle_singleton_instance.get_data(sql=query)

        bank_info_result = [
            GetBankCode.normalize_bank_code(result) for result in bank_code_result
        ]

        return bank_info_result
