# Standard Libs
import pytest
from unittest.mock import patch

# Internal Libs
import api.services.list_client_orders.list_client_orders
from api.services.list_client_orders.list_client_orders import ListOrders
from tests.stubs.project_stubs.stub_data import (StubCompanyInformationRepository,
                                                 payload_data_dummy,
                                                 user_jwt_dummy,
                                                 portfolios_jwt_dummy)
from tests.stubs.project_stubs.stub_list_client_orders import (
    single_client_orders_response,
    list_client_orders_response,
    user_trade_dummy,
    field_dummy,
    normalized_data_dummy,
    list_client_orders_dummy,
    list_client_orders_request_dummy
)


list_data_dummy = ['NEW', 'FILLED']


def test_when_sending_two_order_status_then_return_the_splited_data_as_expected():
    data_to_split = 'NEW|FILLED'
    pipe_to_list_response = ListOrders.pipe_to_list(data=data_to_split)
    assert pipe_to_list_response == list_data_dummy
    assert isinstance(pipe_to_list_response, list)


def test_when_sending_user_trade_and_field_to_decimal_converter_then_return_the_expected():
    response = ListOrders.decimal_128_converter(user_trade=user_trade_dummy,
                                                field=field_dummy)
    assert response == 0.0
    assert type(response) is int


@pytest.mark.asyncio
@patch('api.services.list_client_orders.list_client_orders.CompanyInformationRepository.get_company_name',
       return_value='Iochpe Maxion SA')
async def test_when_sending_the_user_trade_params_then_return_the_normalized_data(mock_normalize_open_order):
    response = await ListOrders.normalize_open_order(user_trade=user_trade_dummy)
    assert response == normalized_data_dummy
    mock_normalize_open_order.assert_called_with('MYPK3')
    assert isinstance(response, dict)


@pytest.mark.asyncio
@patch('api.repositories.companies_data.repository.CompanyInformationRepository.get_company_name')
async def test_when_sending_the_right_params_to_get_company_name_then_return_the_expected(mock_get_company_name):
    symbol_dummy = 'MYPK3'
    ListOrders.company_information_repository = StubCompanyInformationRepository
    response = await ListOrders.company_information_repository.get_company_name(symbol=symbol_dummy)
    assert response == 'Iochpe Maxion SA'
    assert isinstance(response, str)


@pytest.mark.asyncio
@patch('api.repositories.companies_data.repository.CompanyInformationRepository.get_company_name')
async def test_when_sending_the_right_params_to_get_company_name_then_return_the_expected(mock_get_company_name):
    symbol_dummy = None
    ListOrders.company_information_repository = StubCompanyInformationRepository
    response = await ListOrders.company_information_repository.get_company_name(symbol=symbol_dummy)
    assert response is None


# @pytest.mark.asyncio
# @patch('api.services.list_client_orders.list_client_orders.open_orders.oracle_singleton_instance.get_data',
#        return_value=)
# async def test_when_sending_the_right_params_and_single_order_status_then_return_the_expected():
#     response = await ListOrders.get_service_response(jwt_data=payload_data_dummy,
#                                                      list_client_orders=list_client_orders_request_dummy)
#     assert response == single_client_orders_response
#     assert response[0]['symbol'] == 'LALA3'
#     assert isinstance(response, list)
#
#
# @pytest.mark.asyncio
# @patch.object(ListOrders, 'get_service_response', return_value=list_client_orders_response)
# async def test_when_sending_the_right_params_and_two_order_status_then_return_the_expected(
#         mock_get_service_response):
#     response = await ListOrders.get_service_response(jwt_data=payload_data_dummy,
#                                                      list_client_orders=list_client_orders_dummy)
#     assert response == list_client_orders_response
#     assert response[0]['symbol'] == 'MYPK3'
#     assert response[1]['symbol'] == 'BAZA3'
#     assert isinstance(response, list)
#
#
# @pytest.mark.asyncio
# @patch.object(ListOrders, 'get_service_response', return_value=[{}])
# async def test_when_sending_wrong_params_then_return_an_empty_object(mock_get_service_response):
#     client_orders = {'region': '',
#                      'offset': 0,
#                      'limit': 1,
#                      'order_status': ''}
#     response = await ListOrders.get_service_response(jwt_data=payload_data_dummy,
#                                                      list_client_orders=client_orders)
#     assert response == [{}]
#
#
# @pytest.mark.asyncio
# @patch.object(ListOrders, "get_service_response")
# async def test_when_jwt_data_payload_is_valid_then_check_if_the_user_is_in_the_payload_response(
#         mock_get_service_response):
#     response = await ListOrders.get_service_response(list_client_orders=list_client_orders_dummy,
#                                                      jwt_data=payload_data_dummy)
#     jwt = payload_data_dummy.get("user")
#     assert response is not None
#     assert jwt == user_jwt_dummy
#     assert isinstance(jwt, dict)
#     mock_get_service_response.assert_called()
#
#
# @pytest.mark.asyncio
# @patch.object(ListOrders, "get_service_response")
# async def test_when_jwt_data_payload_is_valid_then_check_if_portfolios_is_in_the_payload_response(
#         mock_get_service_response):
#     response = await ListOrders.get_service_response(list_client_orders=list_client_orders_dummy,
#                                                      jwt_data=payload_data_dummy)
#     jwt = payload_data_dummy["user"]["portfolios"]
#     assert response is not None
#     assert jwt == portfolios_jwt_dummy
#     assert isinstance(jwt, dict)
#     mock_get_service_response.assert_called()
#
#
# @pytest.mark.asyncio
# @patch.object(ListOrders, "get_service_response", return_value=Exception)
# async def test_when_jwt_data_payload_is_invalid_then_check_if_portfolios_is_in_the_payload_response(
#         mock_get_service_response):
#     payload_dummy = ""
#     response = await ListOrders.get_service_response(list_client_orders=list_client_orders_dummy,
#                                                      jwt_data=payload_dummy)
#     assert response == Exception
#
#
# @pytest.mark.asyncio
# @patch.object(ListOrders, "get_service_response")
# async def test_if_the_jwt_is_valid_then_return_the_expected(mock_get_service_response):
#     response = await ListOrders.get_service_response(list_client_orders=list_client_orders_dummy,
#                                                      jwt_data=payload_data_dummy)
