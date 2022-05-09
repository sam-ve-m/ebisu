# Standard Libs
import pytest
from unittest.mock import patch, MagicMock


# External Libs
from api.repositories.files.repository import FileRepository
from api.services.list_broker_note.list_broker_note import ListBrokerNote
from api.domain.validators.exchange_info.list_broker_note_validator import (BrokerNoteMarket,
                                                                            BrokerNoteRegion)
from tests.api.stubs.project_stubs.stub_data import (
                                                    payload_data_dummy,
                                                    StubS3Connection,
                                                    payload_data_us_gringa_dummy)
from tests.api.stubs.project_stubs.stub_broker_note_pdf import (
                                                    file_link_brokerage_dummy,
                                                    broker_note_link_dummy,
                                                    month_broker_note_bmf_dummy,
                                                    broker_note_us_link_dummy,
                                                    month_broker_note_dummy,
                                                    month_broker_note_us_dummy,
                                                    directories, broker_note_link_all_dummy,
                                                    all_broker_note_from_all_markets_dummy,
                                                    month_broker_note_all_br_dummy,
                                                    broker_note_from_br_markets_dummy
                                                )


@patch.object(ListBrokerNote, 'generate_path', return_value="'LXPD000001/US/broker_note/2022/4/'")
@patch.object(FileRepository, 'generate_file_link', return_value=broker_note_us_link_dummy)
@patch.object(ListBrokerNote, 'get_broker_note_file_name', return_value=5)
@patch.object(ListBrokerNote, 'get_month_broker_notes', return_value=month_broker_note_us_dummy)
@patch.object(FileRepository, 'list_all_directories_in_path', return_value=directories)
def test_when_params_are_valid_for_us_market_then_get_broker_note_link_as_expected_for_us_account(
        mock_list_all_directories_in_path,
        mock_get_month_broker_notes,
        mock_get_broker_note_file_name,
        mock_generate_file_link,
        mock_generate_path):
    response = ListBrokerNote.get_service_response(
        broker_note=MagicMock(region='US',
                              market=BrokerNoteMarket.US,
                              year=2022,
                              month=4),
        jwt_data=payload_data_us_gringa_dummy)
    mock_get_month_broker_notes.assert_called_with(market=BrokerNoteMarket.US,
                                                   region='US',
                                                   month_broker_notes_directories=directories)

    assert response == month_broker_note_us_dummy
    assert response[0]['market'] == "us"


@patch.object(ListBrokerNote, 'generate_path', return_value="'000000014-6/BR/broker_note/2022/4/'")
@patch.object(FileRepository, 'generate_file_link', return_value=broker_note_link_dummy)
@patch.object(ListBrokerNote, 'get_broker_note_file_name', return_value=5)
@patch.object(ListBrokerNote, 'get_month_broker_notes', return_value=month_broker_note_bmf_dummy)
@patch.object(FileRepository, 'list_all_directories_in_path', return_value=directories)
def test_when_jwt_data_and_broker_note_is_valid_to_bmf_market_then_return_the_response_to_get_broker_note_for_br_account(
        mock_list_all_directories_in_path,
        mock_get_month_broker_notes,
        mock_get_broker_note_file_name,
        mock_generate_file_link,
        mock_generate_path,):
    response_bmf = ListBrokerNote.get_service_response(
        broker_note=MagicMock(region='BR',
                              market=BrokerNoteMarket.BMF,
                              year=2022,
                              month=4),
        jwt_data=payload_data_dummy)
    mock_get_month_broker_notes.assert_called_with(market=BrokerNoteMarket.BMF,
                                                   region='BR',
                                                   month_broker_notes_directories=directories)

    assert response_bmf == month_broker_note_bmf_dummy
    assert response_bmf[0]['market'] == "bmf"


@patch.object(ListBrokerNote, 'generate_path', return_value="'000000014-6/BR/broker_note/2022/4/'")
@patch.object(FileRepository, 'generate_file_link', return_value=broker_note_link_dummy)
@patch.object(ListBrokerNote, 'get_broker_note_file_name', return_value=5)
@patch.object(ListBrokerNote, 'get_month_broker_notes', return_value=month_broker_note_dummy)
@patch.object(FileRepository, 'list_all_directories_in_path', return_value=directories)
def test_when_jwt_data_and_broker_note_is_valid_to_bovespa_market_then_return_the_response_to_get_broker_note_for_br_account(
        mock_list_all_directories_in_path,
        mock_get_month_broker_notes,
        mock_get_broker_note_file_name,
        mock_generate_file_link,
        mock_generate_path,):
    response = ListBrokerNote.get_service_response(
        broker_note=MagicMock(region='BR',
                              market=BrokerNoteMarket.BOVESPA,
                              year=2022,
                              month=4),
        jwt_data=payload_data_dummy)
    mock_get_month_broker_notes.assert_called_with(market=BrokerNoteMarket.BOVESPA,
                                                   region='BR',
                                                   month_broker_notes_directories=directories)

    assert response == month_broker_note_dummy
    assert response[0]['market'] == "bovespa"


@patch.object(ListBrokerNote, 'generate_path', return_value="'000000014-6/ALL/broker_note/2022/4/'")
@patch.object(FileRepository, 'generate_file_link', return_value=broker_note_link_all_dummy)
@patch.object(ListBrokerNote, 'get_broker_note_file_name', return_value=5)
@patch.object(ListBrokerNote, 'get_month_broker_notes', return_value=month_broker_note_us_dummy)
@patch.object(FileRepository, 'list_all_directories_in_path', return_value=directories)
def test_when_jwt_data_and_broker_note_is_valid_to_bovespa_market_then_return_the_response_to_get_broker_note_for_br_account(
        mock_list_all_directories_in_path,
        mock_get_month_broker_notes,
        mock_get_broker_note_file_name,
        mock_generate_file_link,
        mock_generate_path):
    response = ListBrokerNote.get_service_response(
        broker_note=MagicMock(region=BrokerNoteRegion.ALL,
                              market=BrokerNoteMarket.ALL,
                              year=2022,
                              month=4),
        jwt_data=payload_data_us_gringa_dummy)

    assert response == all_broker_note_from_all_markets_dummy
    assert response[0]['market'] == "us"


@patch.object(ListBrokerNote, 'generate_path', return_value="'000000014-6/BR/broker_note/2022/4/'")
@patch.object(FileRepository, 'generate_file_link', return_value=broker_note_link_dummy)
@patch.object(ListBrokerNote, 'get_broker_note_file_name', return_value=5)
@patch.object(ListBrokerNote, 'get_month_broker_notes', return_value=month_broker_note_all_br_dummy)
@patch.object(FileRepository, 'list_all_directories_in_path', return_value=directories)
def test_when_jwt_data_and_broker_note_is_valid_to_all_market_and_br_then_return_the_response_to_get_broker_note_for_br_account(
        mock_list_all_directories_in_path,
        mock_get_month_broker_notes,
        mock_get_broker_note_file_name,
        mock_generate_file_link,
        mock_generate_path):
    response = ListBrokerNote.get_service_response(
        broker_note=MagicMock(region=BrokerNoteRegion.BR,
                              market=BrokerNoteMarket.ALL,
                              year=2022,
                              month=4),
        jwt_data=payload_data_dummy)

    assert response == broker_note_from_br_markets_dummy
    assert response[0]['market'] == "all"


@patch.object(ListBrokerNote, 'generate_path', return_value="'000000014-6/US/broker_note/2022/4/'")
@patch.object(FileRepository, 'generate_file_link', return_value=broker_note_us_link_dummy)
@patch.object(ListBrokerNote, 'get_broker_note_file_name', return_value=5)
@patch.object(ListBrokerNote, 'get_month_broker_notes', return_value=month_broker_note_us_dummy)
@patch.object(FileRepository, 'list_all_directories_in_path', return_value=directories)
def test_when_jwt_data_and_broker_note_is_valid_to_bovespa_market_then_return_the_response_to_get_broker_note_for_br_account(
        mock_list_all_directories_in_path,
        mock_get_month_broker_notes,
        mock_get_broker_note_file_name,
        mock_generate_file_link,
        mock_generate_path):
    response = ListBrokerNote.get_service_response(
        broker_note=MagicMock(region=BrokerNoteRegion.ALL,
                              market=BrokerNoteMarket.US,
                              year=2022,
                              month=4),
        jwt_data=payload_data_us_gringa_dummy)

    assert response == month_broker_note_us_dummy
    assert response[0]['market'] == "us"


@pytest.mark.asyncio
async def test_when_sending_the_right_file_path_then_return_a_valid_generated_file_link():
    file_path = f"{'49'}/{'BR'}/broker_note/{'2021'}/{'10'}/{'5'}.pdf"
    ListBrokerNote.s3_singleton = StubS3Connection
    response = ListBrokerNote.s3_singleton.generate_file_link(file_path=file_path)
    assert response == file_link_brokerage_dummy


def test_when_not_passing_either_jwt_and_broker_note_params_to_request_body_then_return_attr_error():
    with pytest.raises(AttributeError) as err:
        ListBrokerNote.get_service_response(jwt_data="", broker_note="")
        assert err == "'str' object has no attribute 'get'"


def test_when_params_of_broker_note_pydantic_are_invalid_then_raise_attr_error():
    with pytest.raises(AttributeError) as err:
        ListBrokerNote.get_service_response(jwt_data=payload_data_dummy, broker_note="")
        assert err == "AttributeError: 'str' object has no attribute 'region'"
