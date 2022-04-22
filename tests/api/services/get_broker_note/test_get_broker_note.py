# Standard Libs
import pytest
from unittest.mock import patch

# External Libs
from api.services.get_broker_note.get_broker_note import GetBrokerNotePDF
from tests.stubs.stub_jwt.stub_data import (
    payload_data_stub,
    user_jwt_stub,
    portfolios_jwt_stub,
    broker_note_pdf_stub_br,
    wrong_broker_note_pdf_stub_br,
    broker_note_link_pdf_stub)


@pytest.mark.asyncio
@patch.object(GetBrokerNotePDF, "get_service_response", return_value=broker_note_pdf_stub_br)
def test_when_jwt_data_payload_is_valid_then_check_if_the_user_is_in_the_payload_response_for_get_broker_note(
        mock_get_service_response):
    response = GetBrokerNotePDF.get_service_response(broker_note_pdf=broker_note_pdf_stub_br,
                                                     jwt_data=payload_data_stub)
    jwt = payload_data_stub.get("user")
    assert response is not None
    assert jwt == user_jwt_stub
    assert isinstance(jwt, dict)
    mock_get_service_response.assert_called()


@pytest.mark.asyncio
@patch.object(GetBrokerNotePDF, "get_service_response", return_value=broker_note_pdf_stub_br)
def test_when_jwt_data_payload_is_valid_then_check_if_portfolios_is_in_the_payload_response(
        mock_get_service_response):
    response = GetBrokerNotePDF.get_service_response(broker_note_pdf=broker_note_pdf_stub_br,
                                                     jwt_data=payload_data_stub)
    jwt = payload_data_stub["user"]["portfolios"]
    assert response == broker_note_pdf_stub_br
    assert jwt == portfolios_jwt_stub
    assert isinstance(jwt, dict)
    mock_get_service_response.assert_called()
    mock_get_service_response.assert_called_once()


@pytest.mark.asyncio
@patch.object(GetBrokerNotePDF, "get_service_response", return_value=Exception)
def test_when_jwt_data_payload_is_not_valid_then_return_exception(mock_get_service_response):
    wrong_payload_data_stub = {}
    response = GetBrokerNotePDF.get_service_response(broker_note_pdf=broker_note_pdf_stub_br,
                                                     jwt_data=wrong_payload_data_stub)
    assert response == Exception
    mock_get_service_response.assert_called()


@pytest.mark.asyncio
@patch.object(GetBrokerNotePDF, "get_service_response", return_value=Exception)
def test_when_broker_note_pydantic_is_missing_any_required_param_then_return_exception(mock_get_service_response):
    response = GetBrokerNotePDF.get_service_response(broker_note_pdf=wrong_broker_note_pdf_stub_br,
                                                     jwt_data=payload_data_stub)
    assert response == Exception


@pytest.mark.asyncio
@patch.object(GetBrokerNotePDF, "get_service_response", return_value=Exception)
def test_when_broker_note_pydantic_and_jwt_is_missing_any_required_param_then_return_exception(
        mock_get_service_response):
    payload = {}
    response = GetBrokerNotePDF.get_service_response(broker_note_pdf=wrong_broker_note_pdf_stub_br,
                                                     jwt_data=payload)
    assert response == Exception


@pytest.mark.asyncio
@patch.object(GetBrokerNotePDF, "get_service_response", return_value=broker_note_link_pdf_stub)
def test_when_params_and_jwt_are_valid_then_return_the_broker_note_link_as_expected(mock_get_service_response):
    response = GetBrokerNotePDF.get_service_response(broker_note_pdf=broker_note_pdf_stub_br,
                                                     jwt_data=payload_data_stub)
    assert response is not None
    assert response == broker_note_link_pdf_stub


@pytest.mark.asyncio
@patch.object(GetBrokerNotePDF, "get_service_response", return_value=broker_note_link_pdf_stub)
def test_when_sending_the_right_params_then_returning_the_pdf_link_to_broker_note(mock_get_service_response):
    response = GetBrokerNotePDF.get_service_response(broker_note_pdf=broker_note_pdf_stub_br,
                                                     jwt_data=payload_data_stub)
    assert response == broker_note_link_pdf_stub
    assert 'pdf_link' in broker_note_link_pdf_stub
    mock_get_service_response.assert_called_once()
