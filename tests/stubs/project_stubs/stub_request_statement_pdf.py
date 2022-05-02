# Standard Libs
import pytest
from unittest.mock import patch, MagicMock

# External Libs
from api.repositories.files.repository import FileRepository
from api.services.request_statement.request_statement import RequestStatement
from tests.stubs.project_stubs.stub_data import (
                                                    payload_data_dummy,
                                                    StubS3Connection)


@pytest.mark.asyncio
def test_generate_path_function_when_sending_the_right_params_then_return_the_expected():
    response = RequestStatement.generate_path(client_id=None,
                                              start_date=1646757399000,
                                              end_date=1648485399000)
    expected_response = 'None/statements/1646757399000-1648485399000.pdf'
    assert response == expected_response
    assert isinstance(response, str)


@pytest.mark.asyncio
def test_when_params_of_generate_path_are_none_then_raise_exception_error():
    with pytest.raises(Exception) as err:
        response = RequestStatement.generate_path(  client_id=None,
                                                    start_date=None,
                                                    end_date=None)
        assert err == response


@pytest.mark.asyncio
def test_when_right_params_are_sent_to_generate_pdf_function_then_return_the_expected():
    pass