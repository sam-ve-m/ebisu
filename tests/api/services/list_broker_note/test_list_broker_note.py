# Standard Libs
import pytest
from unittest.mock import patch, MagicMock

# External Libs
from api.domain.validators.exchange_info.list_broker_note_validator import BrokerNoteMarket
from api.repositories.files.repository import FileRepository
from api.services.list_broker_note.list_broker_note import ListBrokerNote
from tests.stubs.project_stubs.stub_broker_note_pdf import (
    file_link_brokerage_dummy,
    broker_note_link_dummy,
    brokerage_note_dummy,
    broker_note_us_link_dummy, list_broker_note_dummy)
from tests.stubs.project_stubs.stub_data import (
                                                    payload_data_dummy,
                                                    StubS3Connection)

month_broker_note_dummy = [{'market': 'bmf', 'region': 'BR', 'day': 5, 'broker_note_link': 'https://brokerage-note-and-bank-statement.s3.amazonaws.com/14/BR/broker_note/2022/4/5.pdf?AWSAccessKeyId=AKIATZVFXI25USQWCS5O&Signature=d9vYYouHGiwtQptZIBZQCOpszj4%3D&Expires=1651608773'}]
directories = MagicMock()

# ------- refazer
@pytest.mark.asyncio
@patch.object(ListBrokerNote, 'generate_path', return_value="'000000014-6/BR/broker_note/2022/4/'")
@patch.object(FileRepository, 'generate_file_link', return_value=broker_note_link_dummy)
@patch.object(ListBrokerNote, 'get_broker_note_file_name', return_value=5)
@patch.object(ListBrokerNote, 'get_month_broker_notes', return_value=month_broker_note_dummy)
@patch.object(FileRepository, 'list_all_directories_in_path', return_value=directories)
def test_when_jwt_data_payload_is_valid_then_return_the_response_to_get_broker_note_for_br_account(
        mock_generate_path, mock_generate_file_link, mock_get_broker_note_file_name, mock_get_month_broker_notes, mock_list_all_directories_in_path):
    response = ListBrokerNote.get_service_response(
        broker_note=MagicMock(region=MagicMock(value='BR'),
                              market=BrokerNoteMarket.BOVESPA,
                              year=2022,
                              month=4),
        jwt_data=payload_data_dummy)
    assert response == list_broker_note_dummy


# # ---- refazer
# @pytest.mark.asyncio
# @patch.object(FileRepository, 'generate_file_link', return_value=broker_note_us_link_dummy)
# def test_when_params_are_valid_for_us_then_get_broker_note_link_as_expected_for_us_account(
#         mock_generate_file_link):
#     response = ListBrokerNote.get_service_response(
#         broker_note=MagicMock(region=MagicMock(value='US'), year=2022, month=10, day=4),
#         jwt_data=payload_data_dummy)
#     assert response == {'pdf_link': broker_note_us_link_dummy}
#     mock_generate_file_link.assert_called_once()


@pytest.mark.asyncio
async def test_when_sending_the_right_file_path_then_return_a_valid_generated_file_link():
    file_path = f"{'49'}/{'BR'}/broker_note/{'2021'}/{'10'}/{'5'}.pdf"
    ListBrokerNote.s3_singleton = StubS3Connection
    response = ListBrokerNote.s3_singleton.generate_file_link(file_path=file_path)
    assert response == file_link_brokerage_dummy


@pytest.mark.asyncio
@patch.object(FileRepository, 'generate_file_link', return_value="")
def test_when_broker_note_params_are_missing_then_return_exception_as_expected(mock_generate_file_link):
    with pytest.raises(Exception) as err:
        ListBrokerNote.get_service_response(broker_note=MagicMock(
                                                                        region=MagicMock(value=''),
                                                                        year=None,
                                                                        month=20,
                                                                        day=4),
                                                                        jwt_data=payload_data_dummy)
        assert err == Exception


@pytest.mark.asyncio
@patch.object(FileRepository, 'generate_file_link', return_value="")
def test_when_broker_note_jwt_data_is_missing_then_raise_attr_error_as_expected(mock_generate_file_link):
    with pytest.raises(AttributeError) as err:
        ListBrokerNote.get_service_response(broker_note=MagicMock(  region=MagicMock(value='BR'),
                                                                    year=2021,
                                                                    month=20,
                                                                    day=4),
                                                                    jwt_data="")
        assert err == AttributeError


@pytest.mark.asyncio
def test_when_not_passing_either_jwt_and_broker_note_params_to_request_body_then_return_attr_error():
    with pytest.raises(AttributeError) as err:
        ListBrokerNote.get_service_response(jwt_data="", broker_note="")
        assert err == "'str' object has no attribute 'get'"


@pytest.mark.asyncio
def test_when_params_of_broker_note_pydantic_are_invalid_then_raise_attr_error():
    with pytest.raises(AttributeError) as err:
        ListBrokerNote.get_service_response(jwt_data=payload_data_dummy, broker_note="")
        assert err == "AttributeError: 'str' object has no attribute 'region'"
