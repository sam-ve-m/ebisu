# Standard Libs
import pytest
from unittest.mock import patch

# External Libs
from api.services.get_broker_note.get_broker_note import GetBrokerNotePDF
from tests.stubs.project_stubs.stub_broker_note_pdf import (
                                                broker_note_pdf_dummy_br,
                                                wrong_broker_note_pdf_dummy_br,
                                                broker_note_link_pdf_dummy,
                                                file_link_brokerage_dummy)
from tests.stubs.project_stubs.stub_data import (payload_data_dummy,
                                                 user_jwt_dummy,
                                                 portfolios_jwt_dummy,
                                                 StubS3Connection)


@pytest.mark.asyncio
@patch('api.services.get_broker_note.get_broker_note.GetBrokerNotePDF.get_service_response',
       return_value=broker_note_link_pdf_dummy)
def test_when_jwt_data_payload_is_valid_then_check_if_the_user_is_in_the_payload_response_for_get_broker_note(
        mock_get_service_response):
    response = mock_get_service_response(broker_note_pdf=broker_note_pdf_dummy_br,
                                         jwt_data=payload_data_dummy)
    jwt = payload_data_dummy.get("user")
    assert jwt == user_jwt_dummy
    assert response == broker_note_link_pdf_dummy
    assert isinstance(jwt, dict)
    mock_get_service_response.assert_called()


@pytest.mark.asyncio
@patch.object(GetBrokerNotePDF, "get_service_response", return_value=broker_note_link_pdf_dummy)
def test_when_jwt_data_payload_is_valid_then_check_if_portfolios_is_in_the_payload_response(
        mock_get_service_response):
    response = GetBrokerNotePDF.get_service_response(broker_note_pdf=broker_note_pdf_dummy_br,
                                                     jwt_data=broker_note_pdf_dummy_br)
    jwt = payload_data_dummy["user"]["portfolios"]
    assert jwt == portfolios_jwt_dummy
    assert response == broker_note_link_pdf_dummy
    assert isinstance(jwt, dict)
    mock_get_service_response.assert_called()
    mock_get_service_response.assert_called_once()


@pytest.mark.asyncio
@patch.object(GetBrokerNotePDF, "get_service_response", return_value=broker_note_link_pdf_dummy)
def test_when_params_and_jwt_are_valid_then_return_the_broker_note_link_as_expected(mock_get_service_response):
    response = GetBrokerNotePDF.get_service_response(broker_note_pdf=broker_note_pdf_dummy_br,
                                                     jwt_data=payload_data_dummy)
    assert response == broker_note_link_pdf_dummy
    mock_get_service_response.assert_called_once()


@pytest.mark.asyncio
@patch('api.services.get_broker_note.get_broker_note.GetBrokerNotePDF.get_service_response',
       return_value=broker_note_link_pdf_dummy)
def test_when_sending_the_right_params_then_returning_the_pdf_link_to_broker_note(mock_get_service_response):
    file_link_dummy = 'https://brokerage-note-and-bank-statement.s3.amazonaws.com/109/?AWSAccessKeyId=5243792748DGHDJDH' \
                      '&signature=FHDGKFU6356489nfhjd65243&expires=875342628946'
    response = GetBrokerNotePDF.get_service_response(broker_note_pdf=broker_note_pdf_dummy_br,
                                                     jwt_data=payload_data_dummy)
    assert 'pdf_link' in response
    assert response['pdf_link'] == file_link_dummy


@pytest.mark.asyncio
@patch('api.services.get_broker_note.get_broker_note.GetBrokerNotePDF.get_service_response',
       return_value=broker_note_link_pdf_dummy)
async def test_when_sending_the_right_file_path_then_return_a_valid_generated_file_link(mock_get_data):
    file_path = f"{'49'}/{'BR'}/broker_note/{'2021'}/{'10'}/{'5'}.pdf"
    GetBrokerNotePDF.s3_singleton = StubS3Connection
    response = GetBrokerNotePDF.s3_singleton.generate_file_link(file_path=file_path)
    assert response == file_link_brokerage_dummy


@pytest.mark.asyncio
@patch.object(GetBrokerNotePDF, "get_service_response", return_value=Exception)
def test_when_broker_note_pydantic_is_missing_any_required_param_then_return_exception(mock_get_service_response):
    response = GetBrokerNotePDF.get_service_response(broker_note_pdf=wrong_broker_note_pdf_dummy_br,
                                                     jwt_data=payload_data_dummy)
    assert response == Exception


@pytest.mark.asyncio
@patch.object(GetBrokerNotePDF, "get_service_response", return_value=Exception)
def test_when_broker_note_pydantic_and_jwt_is_missing_any_required_param_then_return_exception(
        mock_get_service_response):
    payload = {}
    response = GetBrokerNotePDF.get_service_response(broker_note_pdf=wrong_broker_note_pdf_dummy_br,
                                                     jwt_data=payload)
    assert response == Exception


@pytest.mark.asyncio
@patch.object(GetBrokerNotePDF, "get_service_response", return_value=Exception)
def test_when_jwt_data_payload_is_not_valid_then_return_exception(mock_get_service_response):
    wrong_payload_data_stub = {}
    response = GetBrokerNotePDF.get_service_response(broker_note_pdf=broker_note_pdf_dummy_br,
                                                     jwt_data=wrong_payload_data_stub)
    assert response == Exception
    mock_get_service_response.assert_called()
