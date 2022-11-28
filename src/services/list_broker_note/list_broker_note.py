# STANDARD LIBS
import os
from http import HTTPStatus
from operator import itemgetter
from fastapi import Response
from datetime import datetime

from etria_logger import Gladsheim

# EXTERNAL LIBS
from src.domain.broker_note.us.request.model import (
    ConfirmationRequest,
    ConfimationQueryParams,
    GetStatementRequest,
)
from src.domain.date_formatters.region.enum.date_format.enum import RegionDateFormat
from src.domain.enums.response.internal_code import InternalCode
from src.domain.exceptions.service.broker_note.model import MarketOptionNotImplemented
from src.domain.models.database.list_broker_note.model import BrokerNoteModel
from src.domain.models.response.list_broker_note.response_model import (
    ListBrokerNoteBrResponse,
)
from src.domain.responses.http_response_model import ResponseModel
from src.repositories.files.repository import FileRepository
from src.domain.request.exchange_info.list_broker_note_validator import (
    ListBrokerNoteBrModel,
    BrokerNoteMarket,
    ListBrokerNoteUsModel,
    BrokerNoteRegion,
    GetBrokerNoteUsModel,
)
from src.transport.drive_wealth.confirmation.transport import DwConfirmationTransport


class ListBrokerNote:

    FileRepository = FileRepository

    @staticmethod
    def get_broker_file_notes(
        account: str,
        market: BrokerNoteMarket,
        broker_note: ListBrokerNoteBrModel,
    ):
        file_path = ListBrokerNote.generate_path(
            account=account, broker_note=broker_note
        )

        month_broker_notes_directories = (
            ListBrokerNote.FileRepository.list_all_directories_in_path(
                file_path=file_path
            )
        )
        bovespa_files_data = ListBrokerNote.get_month_broker_notes(
            market=market,
            month_broker_notes_directories=month_broker_notes_directories,
        )
        return bovespa_files_data

    @staticmethod
    def get_bovespa_files_data_of_br_region(
        jwt_data: dict, broker_note: ListBrokerNoteBrModel
    ):
        account = (
            jwt_data.get("user", {})
            .get("portfolios", {})
            .get("br", {})
            .get("bovespa_account")
        )

        bovespa_response = ListBrokerNote.get_broker_file_notes(
            account=account,
            broker_note=broker_note,
            market=BrokerNoteMarket.BOVESPA,
        )
        return bovespa_response

    @staticmethod
    def get_bmf_files_data_of_br_region(
        jwt_data: dict, broker_note: ListBrokerNoteBrModel
    ):
        account = (
            jwt_data.get("user", {})
            .get("portfolios", {})
            .get("br", {})
            .get("bmf_account")
        )

        bmf_response = ListBrokerNote.get_broker_file_notes(
            account=account,
            broker_note=broker_note,
            market=BrokerNoteMarket.BMF,
        )
        return bmf_response

    @staticmethod
    def get_all_market_files_of_br_regions(
        jwt_data: dict, broker_note: ListBrokerNoteBrModel
    ):
        br_account = jwt_data.get("user", {}).get("portfolios", {}).get("br", {})

        bmf_path, bovespa_path = map(
            ListBrokerNote.generate_path,
            *zip(
                (
                    br_account.get("bmf_account"),
                    BrokerNoteRegion.BR,
                    broker_note,
                ),
                (
                    br_account.get("bovespa_account"),
                    BrokerNoteRegion.BR,
                    broker_note,
                ),
            ),
        )

        month_broker_notes_directories = (
            ListBrokerNote.FileRepository.list_all_directories_in_path(
                file_path=bovespa_path
            )
        )
        bovespa_files_data = ListBrokerNote.get_month_broker_notes(
            market=BrokerNoteMarket.BOVESPA,
            month_broker_notes_directories=month_broker_notes_directories,
        )

        month_broker_notes_directories = (
            ListBrokerNote.FileRepository.list_all_directories_in_path(
                file_path=bmf_path
            )
        )
        bmf_files_data = ListBrokerNote.get_month_broker_notes(
            market=BrokerNoteMarket.BMF,
            month_broker_notes_directories=month_broker_notes_directories,
        )

        all_broker_note_from_all_markets = bovespa_files_data + bmf_files_data

        return all_broker_note_from_all_markets

    @staticmethod
    def get_list_broker_notes_br(
        jwt_data: dict, broker_note: ListBrokerNoteBrModel
    ) -> Response:
        map_key = broker_note.market
        broker_note_possibilities = {
            BrokerNoteMarket.BOVESPA: ListBrokerNote.get_bovespa_files_data_of_br_region,
            BrokerNoteMarket.BMF: ListBrokerNote.get_bmf_files_data_of_br_region,
            BrokerNoteMarket.ALL: ListBrokerNote.get_all_market_files_of_br_regions,
        }
        try:
            broker_note_option = broker_note_possibilities[map_key]
            broker_note_option = broker_note_option(
                jwt_data=jwt_data, broker_note=broker_note
            )
        except KeyError:
            raise MarketOptionNotImplemented()

        response_model = ListBrokerNoteBrResponse.to_response(models=broker_note_option)
        response = ResponseModel(
            success=True, result=response_model, internal_code=InternalCode.SUCCESS
        ).build_http_response(status_code=HTTPStatus.OK)
        return response

    @staticmethod
    def get_month_broker_notes(
        market: BrokerNoteMarket,
        month_broker_notes_directories: dict,
    ):

        has_month_broker_note = month_broker_notes_directories.get("Contents")
        broker_notes = []
        if has_month_broker_note:
            for directory in month_broker_notes_directories.get("Contents"):
                try:
                    broker_note_day = ListBrokerNote.get_broker_note_file_name(
                        directory
                    )
                    broker_note_link = FileRepository.generate_file_link(
                        file_path=directory.get("Key"), url_link_expire_seconds=900
                    )
                    broker_notes.append(
                        {
                            "market": market.value,
                            "region": BrokerNoteRegion.BR.value,
                            "day": broker_note_day,
                            "broker_note_link": broker_note_link,
                        }
                    )
                except Exception as err:
                    raise Gladsheim.error(
                        message=f"get_broker_note_file_name::directory_name:: No directory found, {err}",
                        error=err,
                    )

        broker_notes = sorted(broker_notes, key=itemgetter("day"), reverse=True)
        symbols_financial_indicators = [
            BrokerNoteModel(**symbol) for symbol in broker_notes
        ]
        return symbols_financial_indicators

    @classmethod
    def get_broker_note_file_name(cls, directory: dict):
        directory_name = directory.get("Key").split("/")[-1].replace(".pdf", "")
        return int(directory_name)

    @classmethod
    def generate_path(cls, account: str, broker_note: ListBrokerNoteBrModel):
        path_route = os.path.join(
            *tuple(
                str(path_fragment)
                for path_fragment in (
                    "broker_note",
                    broker_note.year,
                    broker_note.month,
                )
                if path_fragment is not None
            )
        )
        path = f"{account}/{BrokerNoteRegion.BR.value}/{path_route}/"
        return path

    @staticmethod
    async def list_broker_notes_us(
        jwt_data: dict, broker_note: ListBrokerNoteUsModel
    ) -> Response:
        account = (
            jwt_data.get("user", {})
            .get("portfolios", {})
            .get("br", {})
            .get("dw_account")
        )

        from_date = datetime.strftime(
            datetime(year=broker_note.year, month=broker_note.month, day=1),
            RegionDateFormat.US_DATE_FORMAT.value,
        )
        if broker_note.month == 12:
            to_date = datetime.strftime(
                datetime(year=broker_note.year + 1, month=1, day=1),
                RegionDateFormat.US_DATE_FORMAT.value,
            )
        else:
            to_date = datetime.strftime(
                datetime(year=broker_note.year, month=broker_note.month + 1, day=1),
                RegionDateFormat.US_DATE_FORMAT.value,
            )

        confirmation_request = ConfirmationRequest(
            account=account,
            query_params=ConfimationQueryParams(
                from_date=from_date,
                to_date=to_date,
            ),
        )

        confirmations = await DwConfirmationTransport.get_confirmations(
            confirmation_request=confirmation_request
        )
        confirmations_response = [confirms.to_dict() for confirms in confirmations]

        response = ResponseModel(
            success=True,
            result=confirmations_response,
            internal_code=InternalCode.SUCCESS,
        ).build_http_response(status_code=HTTPStatus.OK)
        return response

    @staticmethod
    async def get_broker_note_us(
        jwt_data: dict, broker_note: GetBrokerNoteUsModel
    ) -> Response:
        account = (
            jwt_data.get("user", {})
            .get("portfolios", {})
            .get("br", {})
            .get("dw_account")
        )
        statement_request = GetStatementRequest(
            account=account, file_key=broker_note.file_key
        )

        statement = await DwConfirmationTransport.get_statement(
            statement_request=statement_request
        )
        statement_response = statement.to_dict()

        response = ResponseModel(
            success=True, result=statement_response, internal_code=InternalCode.SUCCESS
        ).build_http_response(status_code=HTTPStatus.OK)
        return response
