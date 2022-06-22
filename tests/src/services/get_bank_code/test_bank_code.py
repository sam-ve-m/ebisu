# Standard Libs
import pytest
from unittest.mock import patch

from src.repositories.bank_code.repository import BankCodeRepository
from src.services.get_bank_code.service import GetBankCode
from tests.src.repositories.bank_account.stubs import bank_code_normalized_stub

bank_code_list_stub = {"CD_BANCO": "070", "NM_BANCO": "BANCO REGIONAL DE BRASILIA"}
response_bank_code = {"code": "070", "description": "BANCO REGIONAL DE BRASILIA"}


def test_when_sending_right_params_to_normalize_bank_code_then_return_normalized_data():
    response = GetBankCode.normalize_bank_code(bank_code_list=bank_code_list_stub)
    assert response == {"code": "070", "description": "BANCO REGIONAL DE BRASILIA"}


@patch.object(BankCodeRepository, "get_bank_code_from_database", return_value=[
    {'CD_BANCO': '070', 'NM_BANCO': "BANCO REGIONAL DE BRASILIA"}])
def test_get_bank_code_from_database_when_sending_right_params_then_return_expected(
        mock_get_all_bank_codes_from_database
):
    response = GetBankCode.get_bank_code_from_database(bank="070")
    assert response == [{'CD_BANCO': '070', 'NM_BANCO': 'BANCO REGIONAL DE BRASILIA'}]
    assert isinstance(response, list)


@patch.object(BankCodeRepository, "get_all_bank_codes_from_database", return_value=bank_code_list_stub)
@patch.object(GetBankCode, "normalize_bank_code", return_value=response_bank_code)
def test_get_service_response_from_get_bank_database_then_return_the_right_response(
    mock_get_all_bank_codes_from_database, mock_normalize_bank_code
):
    response = GetBankCode.get_service_response()

    assert response == bank_code_normalized_stub
