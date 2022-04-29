# Standard Libs
import pytest
from unittest.mock import patch, MagicMock

# External Libs
from api.repositories.files.repository import FileRepository
from api.services.get_broker_note.get_broker_note import GetBrokerNotePDF
from tests.stubs.project_stubs.stub_broker_note_pdf import (
    file_link_brokerage_dummy,
    broker_note_link_dummy,
    brokerage_note_dummy, broker_note_us_link_dummy)
from tests.stubs.project_stubs.stub_data import (payload_data_dummy,
                                                 StubS3Connection)


@pytest.mark.asyncio
@patch.object(FileRepository, 'generate_file_link', return_value=broker_note_link_dummy)
def test_when_jwt_data_payload_is_valid_then_return_the_response_to_get_broker_note(
        mock_generate_file_link):
    response = GetBrokerNotePDF.get_service_response(
        broker_note_pdf=MagicMock(region=MagicMock(value='BR'), year=2021, month=20, day=4),
        jwt_data=payload_data_dummy)
    assert response == brokerage_note_dummy
    mock_generate_file_link.assert_called_once()


@pytest.mark.asyncio
@patch.object(FileRepository, 'generate_file_link', return_value=broker_note_us_link_dummy)
def test_when_params_are_valid_for_us_then_get_broker_note_link_as_expected(
        mock_generate_file_link):
    response = GetBrokerNotePDF.get_service_response(
        broker_note_pdf=MagicMock(region=MagicMock(value='US'), year=2022, month=10, day=4),
        jwt_data=payload_data_dummy)
    assert response == {'pdf_link': broker_note_us_link_dummy}
    mock_generate_file_link.assert_called_once()


@pytest.mark.asyncio
async def test_when_sending_the_right_file_path_then_return_a_valid_generated_file_link():
    file_path = f"{'49'}/{'BR'}/broker_note/{'2021'}/{'10'}/{'5'}.pdf"
    GetBrokerNotePDF.s3_singleton = StubS3Connection
    response = GetBrokerNotePDF.s3_singleton.generate_file_link(file_path=file_path)
    assert response == file_link_brokerage_dummy


@pytest.mark.asyncio
@patch.object(FileRepository, 'generate_file_link', return_value="")
def test_when_broker_note_pydantic_is_missing_any_required_param_then_return_exception(mock_generate_file_link):
    with pytest.raises(Exception):
        response = GetBrokerNotePDF.get_service_response(broker_note_pdf=MagicMock(region=MagicMock(value=''),
                                                                                   year=None,
                                                                                   month=20,
                                                                                   day=4),
                                                         jwt_data=payload_data_dummy)
        return response


@pytest.mark.asyncio
@patch.object(FileRepository, 'generate_file_link', return_value="")
def test_when_broker_note_pydantic_and_jwt_is_missing_any_required_param_then_return_exception(
        mock_generate_file_link):
    payload = {}
    with pytest.raises(Exception):
        response = GetBrokerNotePDF.get_service_response(
            broker_note_pdf=MagicMock(region=MagicMock(value=''),
                                      year=None,
                                      month=20,
                                      day=4), jwt_data=payload)
        return response
