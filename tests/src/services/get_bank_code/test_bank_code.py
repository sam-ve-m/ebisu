# Standard Libs
import pytest
from unittest.mock import patch
from src.services.get_bank_code.service import GetBankCode
from src.repositories.statements.repository import StatementsRepository


bank_code_list_stub = {'CD_BANCO': '070', 'NM_BANCO': 'BANCO REGIONAL DE BRASILIA'}
response_bank_code = {"code": "070", "description": "BANCO REGIONAL DE BRASILIA"}


def test_when_sending_right_params_to_normalize_bank_code_then_return_normalized_data():

    response = GetBankCode.normalize_bank_code(
        bank_code_list=bank_code_list_stub
    )

    assert response == response_bank_code


@patch.object(StatementsRepository, 'get_data', return_value=bank_code_list_stub)
@patch.object(GetBankCode, 'normalize_bank_code', return_value=response_bank_code)
def test_get_service_response_then_return_the_right_response(
        mock_get_data, mock_normalize_bank_code
):
    response = GetBankCode.get_service_response()
    bank_code_response = [{'code': '070', 'description': 'BANCO REGIONAL DE BRASILIA'},
                         {'code': '070', 'description': 'BANCO REGIONAL DE BRASILIA'}]

    assert response == bank_code_response
