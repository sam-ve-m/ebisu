# # Standard Libs
# import pytest
# from unittest.mock import patch, MagicMock
#
# # External Libs
# from api.domain.exception.model import NoPdfFoundError
# from api.repositories.base_repositories.oracle.repository import OracleBaseRepository
# from api.repositories.files.repository import FileRepository
# from api.services.statement.service import Statement
# from tests.api.stubs.project_stubs.stub_data import (payload_data_dummy, payload_data_us_gringa_dummy)
# from api.services.request_statement.request_statement import RequestStatement
# from tests.api.stubs.project_stubs.stub_request_statement_pdf import (bank_statement_pdf_br_dummy,
#                                                                       file_upload_response,
#                                                                       generate_path_response,
#                                                                       file_link_stub,
#                                                                       bank_statement_pdf_us_dummy)
#
#
# def test_generate_path_function_when_sending_the_right_params_then_return_the_expected():
#     response = RequestStatement.generate_path(client_id=None,
#                                               start_date=1646757399000,
#                                               end_date=1648485399000)
#     expected_response = 'None/statements/1646757399000-1648485399000.pdf'
#     assert response == expected_response
#     assert isinstance(response, str)
#
#
# def test_when_params_of_generate_path_are_none_then_raise_exception_error():
#     with pytest.raises(Exception) as err:
#         response = RequestStatement.generate_path(client_id=None,
#                                                   start_date=None,
#                                                   end_date=None)
#         assert err == response
#
#
# @patch.object(RequestStatement, 'generate_path', return_value=generate_path_response)
# @patch.object(FileRepository, 'upload_file', return_value=file_upload_response)
# @patch.object(FileRepository, 'generate_file_link', return_value=file_link_stub)
# def test_generate_pdf_function_when_all_params_are_right_then_return_the_expected(
#         mock_generate_path, mock_upload_file, mock_generate_file_link
# ):
#     response = RequestStatement.generate_pdf(statement={'Extrato': []},
#                                              client_id=None,
#                                              start_date=1646757399000,
#                                              end_date=1648485399000)
#     assert response == bank_statement_pdf_br_dummy
#     assert isinstance(response, dict)
#     assert 'pdf_link' in response
#
#
# @patch.object(RequestStatement, 'generate_path', return_value=None)
# @patch.object(FileRepository, 'upload_file', return_value=None)
# @patch.object(FileRepository, 'generate_file_link', return_value=None)
# def test_generate_pdf_function_when_no_link_is_the_response_then_return_the_expected_no_pdf_found_error(
# mock_generate_path, mock_upload_file, mock_generate_file_link
# ):
#     with pytest.raises(NoPdfFoundError) as err:
#         response = RequestStatement.generate_pdf(statement={},
#                                                  client_id=None,
#                                                  start_date=None,
#                                                  end_date=None)
#         assert err == response
#
#
# @pytest.mark.asyncio
# @patch.object(FileRepository, 'upload_file', return_value=file_upload_response)
# @patch.object(FileRepository, 'generate_file_link', return_value=file_link_stub)
# @patch.object(RequestStatement, 'generate_path', return_value=generate_path_response)
# @patch.object(OracleBaseRepository, 'get_data', return_value=[])
# async def test_when_right_params_for_br_account_are_sent_to_service_response_function_then_return_the_expected(
#         mock_upload_file, mock_generate_path, mock_get_data, mock_generate_file_link
# ):
#     response = await RequestStatement.get_service_response(MagicMock(region=MagicMock(value='BR'),
#                                                                      start_date=1646757399000,
#                                                                      end_date=1648485399000),
#                                                                      jwt_data=payload_data_dummy)
#     assert response == bank_statement_pdf_br_dummy
#     assert isinstance(response, dict)
#
#
# @pytest.mark.asyncio
# @patch.object(FileRepository, 'upload_file', return_value=file_upload_response)
# @patch.object(FileRepository, 'generate_file_link', return_value=file_link_stub)
# @patch.object(RequestStatement, 'generate_path', return_value=generate_path_response)
# @patch.object(OracleBaseRepository, 'get_data', return_value=[])
# @patch.object(Statement, 'get_dw_statement', return_value={"balance": 40000.45, "statements": 20000.0})
# async def test_when_right_params_for_us_account_are_sent_to_service_response_function_then_return_the_expected(
#         mock_upload_file, mock_generate_path, mock_get_data, mock_generate_file_link, mock_get_dw_statement
# ):
#     response = await RequestStatement.get_service_response(MagicMock(region=MagicMock(value='US'),
#                                                                      start_date=1646757399000,
#                                                                      end_date=1648485399000),
#                                                                      jwt_data=payload_data_us_gringa_dummy)
#     assert response == bank_statement_pdf_us_dummy
#     assert isinstance(response, dict)
#
#
# @pytest.mark.asyncio
# async def test_request_statement_get_service_response_when_the_params_are_not_valid_then_raise_error_as_expected():
#     with pytest.raises(AttributeError) as err:
#         await RequestStatement.get_service_response(MagicMock(region=MagicMock(value='US'),
#                                                                      start_date=1646757399000,
#                                                                      end_date=1648485399000),
#                                                                      jwt_data="")
#         assert err == "'str' object has no attribute 'get'"
#
#
# @pytest.mark.asyncio
# async def test_get_service_response_when_the_statement_params_are_not_valid_then_raise_error_as_expected():
#     with pytest.raises(TypeError) as err:
#         await RequestStatement.get_service_response(jwt_data=payload_data_us_gringa_dummy,
#                                                     region=None,
#                                                     start_date=None,
#                                                     end_date=None)
#         assert err == "unsupported operand type(s) for /: 'NoneType' and 'int'"
#         assert err == TypeError
