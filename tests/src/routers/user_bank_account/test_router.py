# Standard Libs
import pytest
from unittest.mock import patch, MagicMock

# INTERNAL LIBS
import logging.config

# PROJECT IMPORTS
from decouple import Config, RepositoryEnv

from src.domain.validators.device_info import DeviceInformationOptional
from src.domain.validators.user_account.bank_account import (
    CreateUserBankAccount,
    UpdateUserBankAccounts,
    DeleteUsersBankAccount,
)
from src.domain.exceptions import UnauthorizedError, BadRequestError
from src.routers.user_bank_accounts.router import UserBankAccountsRouter
from src.routers.user_portfolios.router import UserPortfoliosRouter
from src.services.bank_account.service import UserBankAccountService
from src.services.get_bank_code.service import GetBankCode
from src.services.jwt.service import JwtService
from src.services.stock_portfolios_list.service import UserPortfoliosList

# stubs
from tests.src.stubs.project_stubs.stub_data import payload_data_dummy
from tests.src.stubs.router_exchange_infos.stubs import scope_stub
from tests.src.stubs.bank_account_stubs.stub_get_account import (
    get_accounts_dummy,
    jwt_data_to_create_account,
    jwt_with_bank_account_to_update,
    jwt_with_bank_account_to_delete,
    stock_portfolios_response_dummy,
)
from tests.src.stubs.router_bank_accounts_stubs.stubs import (
    scope_wrong_stub,
    scope_correct_stub,
    x_thebes_bank_tuple,
    create_account_stub,
    update_router_account_stub,
    x_mist_bank_tuple,
    delete_router_account_stub,
)


device_info_stub = {
    "device_name": "iphone",
    "device_model": "13",
    "is_emulator": True,
    "device_operating_system_name": "IOS",
    "os_sdk_version": "45125",
    "device_is_in_root_mode": True,
    "device_network_interfaces": "hahahaha",
    "public_ip": "1548455475221",
    "access_ip": "0000145455545",
    "phone_wifi_ip": "123255444456",
    "geolocation": "Brasil, São Paulo, SP",
}


@pytest.mark.asyncio
@patch.object(
    JwtService, "get_thebes_answer_from_request", return_value=payload_data_dummy
)
@patch.object(
    UserBankAccountService, "get_user_bank_accounts", return_value=get_accounts_dummy
)
async def test_when_getting_the_bank_account_with_a_valid_jwt_then_return_the_bank_accounts(
    mock_get_thebes_answer_from_request, mock_get_user_bank_accounts
):
    response = await UserBankAccountsRouter.get_user_bank_accounts(
        request=MagicMock(
            scope=scope_correct_stub, headers=MagicMock(raw=x_thebes_bank_tuple)
        )
    )
    assert response == get_accounts_dummy
    assert isinstance(response, dict)
    assert (
        response.get("bank_accounts")[1].get("id")
        == "15f11e59-4d44-4939-9bf0-25c1501e3b5d"
    )


@pytest.mark.asyncio
@patch.object(
    JwtService, "get_thebes_answer_from_request", return_value=payload_data_dummy
)
@patch.object(
    UserBankAccountService, "get_user_bank_accounts", return_value={"bank_accounts": []}
)
async def test_when_getting_the_bank_account_with_a_valid_jwt_then_return_no_bank_account_register_in_case_theres_no_ba(
    mock_get_thebes_answer_from_request, mock_get_user_bank_accounts
):
    response = await UserBankAccountsRouter.get_user_bank_accounts(
        request=MagicMock(
            scope=scope_correct_stub, headers=MagicMock(raw=x_thebes_bank_tuple)
        )
    )
    assert response == {"bank_accounts": []}
    assert isinstance(response, dict)
    assert response.get("bank_accounts") == []


@pytest.mark.asyncio
async def test_when_sending_the_wrong_payload_jwt_invalid_to_get_balance_then_raise_unauthorized_error():

    with pytest.raises(UnauthorizedError):
        await UserBankAccountsRouter.get_user_bank_accounts(
            request=MagicMock(scope=scope_wrong_stub)
        )


# create bank account router
@pytest.mark.asyncio
@patch.object(
    JwtService,
    "get_thebes_answer_from_request",
    return_value=jwt_data_to_create_account,
)
@patch.object(
    UserBankAccountService,
    "create_user_bank_accounts",
    return_value={"message": "Created"},
)
async def test_when_getting_the_bank_account_with_a_valid_jwt_then_return_the_bank_accounts(
    mock_get_thebes_answer_from_request, mock_create_user_bank_accounts
):

    response = await UserBankAccountsRouter.create_user_bank_accounts(
        request=MagicMock(
            scope=scope_correct_stub,
            headers=MagicMock(raw=[x_thebes_bank_tuple, x_mist_bank_tuple]),
        ),
        create_bank_account=CreateUserBankAccount(**create_account_stub),
    )

    assert response == {"message": "Created"}


@pytest.mark.asyncio
async def test_when_sending_an_invalid_jwt_to_create_account_then_raise_bad_request_error():

    with pytest.raises(BadRequestError):
        await UserBankAccountsRouter.create_user_bank_accounts(
            request=MagicMock(
                scope=scope_correct_stub, headers=MagicMock(raw=[scope_stub])
            ),
            create_bank_account=CreateUserBankAccount(**create_account_stub),
        )


@pytest.mark.asyncio
async def test_when_sending_an_invalid_param_of_model_to_create_account_then_raise_internal_server_error():

    with pytest.raises(BaseException):
        await UserBankAccountsRouter.create_user_bank_accounts(
            request=MagicMock(
                scope=scope_correct_stub, headers=MagicMock(raw=x_thebes_bank_tuple)
            ),
            create_bank_account=None,
        )


# update user bank account
@pytest.mark.asyncio
@patch.object(
    JwtService,
    "get_thebes_answer_from_request",
    return_value=jwt_with_bank_account_to_update,
)
@patch.object(
    UserBankAccountService,
    "update_user_bank_account",
    return_value={"message": "Updated"},
)
async def test_when_getting_the_bank_account_with_a_valid_jwt_then_return_the_bank_accounts(
    mock_get_thebes_answer_from_request, mock_update_user_bank_account
):

    response = await UserBankAccountsRouter.update_bank_account(
        request=MagicMock(
            scope=scope_correct_stub,
            headers=MagicMock(raw=[x_thebes_bank_tuple, x_mist_bank_tuple]),
        ),
        update_bank_account=UpdateUserBankAccounts(**update_router_account_stub),
    )

    assert response == {"message": "Updated"}


@pytest.mark.asyncio
async def test_when_sending_an_invalid_jwt_to_update_account_then_raise_bad_request_error():

    with pytest.raises(BadRequestError):
        await UserBankAccountsRouter.update_bank_account(
            request=MagicMock(
                scope=scope_correct_stub, headers=MagicMock(raw=[scope_stub])
            ),
            update_bank_account=UpdateUserBankAccounts(**update_router_account_stub),
        )


@pytest.mark.asyncio
async def test_when_sending_an_invalid_param_of_model_to_update_account_then_raise_internal_server_error():

    with pytest.raises(BaseException):
        await UserBankAccountsRouter.update_bank_account(
            request=MagicMock(
                scope=scope_correct_stub, headers=MagicMock(raw=x_thebes_bank_tuple)
            ),
            update_bank_account=None,
        )


# delete user bank account
@pytest.mark.asyncio
@patch.object(
    JwtService,
    "get_thebes_answer_from_request",
    return_value=jwt_with_bank_account_to_delete,
)
@patch.object(
    UserBankAccountService,
    "delete_user_bank_account",
    return_value={"message": "Deleted"},
)
async def test_when_getting_the_bank_account_with_a_valid_jwt_then_return_the_bank_accounts(
    mock_get_thebes_answer_from_request, mock_delete_user_bank_account
):

    response = await UserBankAccountsRouter.delete_bank_account(
        request=MagicMock(
            scope=scope_correct_stub,
            headers=MagicMock(raw=[x_thebes_bank_tuple, x_mist_bank_tuple]),
        ),
        delete_bank_account=MagicMock(
            id="ff302d01-849c-4805-b754-c1636cbbb1f3", device_info=device_info_stub
        ),
    )

    assert response == {"message": "Deleted"}


@pytest.mark.asyncio
async def test_when_sending_an_invalid_jwt_to_delete_account_then_raise_unauthorized_error():

    with pytest.raises(UnauthorizedError):
        await UserBankAccountsRouter.delete_bank_account(
            request=MagicMock(
                scope=scope_correct_stub, headers=MagicMock(raw=[scope_stub])
            ),
            delete_bank_account=MagicMock(
                id="ff302d01-849c-4805-b754-c1636cbbb1f3", device_info=device_info_stub
            ),
        )


@pytest.mark.asyncio
async def test_when_sending_an_invalid_param_of_model_to_delete_account_then_raise_internal_server_error():

    with pytest.raises(BaseException):
        await UserBankAccountsRouter.delete_bank_account(
            request=MagicMock(
                scope=scope_correct_stub, headers=MagicMock(raw=x_thebes_bank_tuple)
            ),
            delete_bank_account=None,
        )


# user stock portfolio list
@pytest.mark.asyncio
@patch.object(
    JwtService, "get_thebes_answer_from_request", return_value=payload_data_dummy
)
@patch.object(
    UserPortfoliosList,
    "get_user_portfolios_response",
    return_value=stock_portfolios_response_dummy,
)
async def test_when_getting_the_stock_portfolios_with_a_valid_jwt_then_return_the_portfolios(
    mock_get_thebes_answer_from_request, mock_get_user_bank_accounts
):
    response = await UserPortfoliosRouter.user_portfolios_list(
        request=MagicMock(
            scope=scope_correct_stub, headers=MagicMock(raw=x_thebes_bank_tuple)
        )
    )
    assert response == stock_portfolios_response_dummy
    assert isinstance(response, dict)


@pytest.mark.asyncio
async def test_when_sending_an_invalid_jwt_to_stock_portfolios_then_raise_unauthorized_error():

    with pytest.raises(UnauthorizedError):
        await UserPortfoliosRouter.user_portfolios_list(
            request=MagicMock(
                scope=scope_wrong_stub, headers=MagicMock(raw=[scope_stub])
            )
        )


response_bank_code = [{"code": "070", "description": "BANCO REGIONAL DE BRASILIA"}]


# bank code and description
@patch.object(GetBankCode, "get_service_response", return_value=response_bank_code)
def test_bank_code_and_description_router_then_return_the_bank_code_list(
    mock_get_service_response,
):
    response = UserBankAccountsRouter.bank_code_and_description()
    assert response == response_bank_code
    assert isinstance(response, list)
