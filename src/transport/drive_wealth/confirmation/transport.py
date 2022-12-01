# STANDARD IMPORTS
import json
from typing import List

# EXTERNAL IMPORTS
from etria_logger import Gladsheim
from mepho import DWApiTransport

# PROJECT IMPORTS
from src.domain.broker_note.us.model import Confirmation, Statement
from src.domain.broker_note.us.request.model import (
    ConfirmationRequest,
    GetStatementRequest,
)
from src.domain.exceptions.transport.drive_wealth.base.model import FailToGetDataFromTransportLayer
from src.infrastructures.env_config import config
from src.transport.drive_wealth.base.transport import DwBaseTransport


class DwConfirmationTransport(DwBaseTransport):
    @staticmethod
    async def __execute_get(url: str, query_params: dict):
        try:
            response = await DWApiTransport.execute_get(url=url, query_params=query_params)
        except Exception as error:
            Gladsheim.error(
                error=error,
                message=f"DwConfirmationTransport::__execute_get::Error to make request",
            )
            raise FailToGetDataFromTransportLayer()
        return response

    @staticmethod
    def __build_confirmation_model(raw_confirmation: dict) -> Confirmation:
        confirmation_model = Confirmation(
            description=raw_confirmation.get("displayName"),
            file_key=raw_confirmation.get("fileKey"),
        )
        return confirmation_model

    @staticmethod
    def __build_statement_model(raw_statement: dict) -> Statement:
        statement_model = Statement(
            broker_note_link=raw_statement.get("url"),
        )
        return statement_model

    @staticmethod
    async def get_confirmations(
        confirmation_request: ConfirmationRequest,
    ) -> List[Confirmation]:
        confirmations = await DwConfirmationTransport.__get_confirmations(
            confirmation_request=confirmation_request
        )
        confirmations_model = [
            DwConfirmationTransport.__build_confirmation_model(
                raw_confirmation=confirmation
            )
            for confirmation in confirmations
        ]
        return confirmations_model

    @classmethod
    async def __get_confirmations(
        cls, confirmation_request: ConfirmationRequest
    ) -> List[dict]:
        confirmation_url = config("DW_CONFIRMATION_URL")

        query_params = confirmation_request.get_query_params()
        account = confirmation_request.get_account()
        url_formatted = confirmation_url.format(account)

        response = await cls.__execute_get(
            url=url_formatted, query_params=query_params
        )

        body = await response.text()
        confirmations = json.loads(body)

        cls._handle_dw_error_status_from_response(
            request=url_formatted, response=confirmations
        )
        cls._handle_http_error_from_drive_wealth_request(
            request=url_formatted, response=response
        )
        return confirmations

    @staticmethod
    async def get_statement(
        statement_request: GetStatementRequest,
    ) -> Statement:
        statement = await DwConfirmationTransport.__get_statement(
            statement_request=statement_request
        )
        statement_model = DwConfirmationTransport.__build_statement_model(
            raw_statement=statement
        )
        return statement_model

    @classmethod
    async def __get_statement(cls, statement_request: GetStatementRequest) -> dict:
        confirmation_url = config("DW_STATEMENT_URL")

        account = statement_request.get_account()
        file_key = statement_request.get_file_key()

        final_url = confirmation_url.format(account, file_key)

        response = await cls.__execute_get(url=final_url, query_params={})

        body = await response.text()
        statement = json.loads(body)

        cls._handle_dw_error_status_from_response(request=final_url, response=statement)
        cls._handle_http_error_from_drive_wealth_request(
            request=final_url, response=response
        )
        return statement

