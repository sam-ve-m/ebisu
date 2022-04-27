# Standard Libs
import pytest
from unittest.mock import patch
from typing import List

# Internal Libs
from api.services.list_client_orders.list_client_orders import ListOrders
from tests.stubs.project_stubs.stub_data import StubCompanyInformationRepository
from tests.stubs.project_stubs.stub_list_client_orders import (
                                                                single_client_orders_response,
                                                                list_client_orders_response,
                                                                user_trade_dummy,
                                                                field_dummy,
                                                                normalized_data_dummy
                                                            )


list_data_dummy = ['NEW', 'FILLED']


@pytest.mark.asyncio
@patch('api.services.list_client_orders.list_client_orders.ListOrders.pipe_to_list', return_value=list_data_dummy)
def test_when_sending_two_order_status_then_return_the_splited_data_as_expected(mock_pipe_to_list):
    data_to_split = 'NEW|CANCELLED'
    pipe_to_list_response = ListOrders.pipe_to_list(data=data_to_split)
    assert pipe_to_list_response == list_data_dummy
    assert isinstance(pipe_to_list_response, list)


@pytest.mark.asyncio
@patch('api.services.list_client_orders.list_client_orders.ListOrders.decimal_128_converter', return_value=0.0)
def test_when_sending_user_trade_and_field_to_decimal_converter_then_return_the_expected(mock_decimal_128_converter):
    response = ListOrders.decimal_128_converter(user_trade=user_trade_dummy,
                                                field=field_dummy)
    assert response == 0.0
    assert type(response) is float


@pytest.mark.asyncio
@patch('api.services.list_client_orders.list_client_orders.ListOrders.normalize_open_order',
       return_value=normalized_data_dummy)
async def test_when_sending_the_user_trade_params_then_return_the_normalized_data(mock_normalize_open_order):
    response = await ListOrders.normalize_open_order(user_trade=user_trade_dummy)
    assert response == normalized_data_dummy
    assert isinstance(response, dict)


@pytest.mark.asyncio
@patch('api.repositorues.companies_data.repository.CompanyInformationRepository.get_company_name', return_value="")
async def test_when_sending_the_right_params_to_get_company_name_then_return_the_expected(mock_get_company_name)
ListOrders.company_information_repository = StubCompanyInformationRepository