from src.repositories.bank_code.repository import BankCodeRepository


class GetBankCode:

    @classmethod
    def normalize_bank_code(cls, bank_code_list: dict) -> dict:

        normalize_data = {
            "code": bank_code_list.get("CD_BANCO"),
            "description": bank_code_list.get("NM_BANCO"),
        }

        return normalize_data

    @classmethod
    def get_bank_code_from_database(cls, bank: str):

        bank_code_result = BankCodeRepository.get_bank_code_from_database(bank=bank)

        return bank_code_result

    @classmethod
    def get_service_response(cls):

        bank_code_result = BankCodeRepository.get_all_bank_codes_from_database()

        bank_info_result = [
            GetBankCode.normalize_bank_code(result) for result in bank_code_result
        ]

        return bank_info_result
