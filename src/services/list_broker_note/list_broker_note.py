# STANDARD LIBS
import os
from operator import itemgetter
from etria_logger import Gladsheim

# EXTERNAL LIBS
from src.repositories.files.repository import FileRepository
from src.domain.validators.exchange_info.list_broker_note_validator import (
    ListBrokerNoteModel,
    BrokerNoteMarket,
    BrokerNoteRegion,
)


class ListBrokerNote:

    FileRepository = FileRepository

    @staticmethod
    def get_bovespa_files_data_of_br_region(jwt_data: dict, broker_note: ListBrokerNoteModel):

        portfolios = jwt_data.get("user", {}).get("portfolios", {})
        br_portfolios = portfolios.get("br", {})

        bovespa_file_path = ListBrokerNote.generate_path(
            account=br_portfolios.get("bovespa_account"),
            region=broker_note.region,
            broker_note=broker_note,
        )
        month_broker_notes_directories = (
            ListBrokerNote.FileRepository.list_all_directories_in_path(
                file_path=bovespa_file_path
            )
        )
        bovespa_files_data = ListBrokerNote.get_month_broker_notes(
            market=BrokerNoteMarket.BOVESPA,
            region=BrokerNoteRegion.BR,
            month_broker_notes_directories=month_broker_notes_directories,
        )
        return bovespa_files_data

    @staticmethod
    def get_bmf_files_data_of_br_region(jwt_data: dict, broker_note: ListBrokerNoteModel):

        portfolios = jwt_data.get("user", {}).get("portfolios", {})
        br_portfolios = portfolios.get("br", {})

        bmf_file_path = ListBrokerNote.generate_path(
            account=br_portfolios.get("bmf_account"),
            region=broker_note.region,
            broker_note=broker_note,
        )
        month_broker_notes_directories = (
            ListBrokerNote.FileRepository.list_all_directories_in_path(
                file_path=bmf_file_path
            )
        )
        bmf_files_data = ListBrokerNote.get_month_broker_notes(
            market=BrokerNoteMarket.BMF,
            region=BrokerNoteRegion.BR,
            month_broker_notes_directories=month_broker_notes_directories,
        )
        return bmf_files_data

    @staticmethod
    def get_dw_files_data_of_us_region(jwt_data: dict, broker_note: ListBrokerNoteModel):

        portfolios = jwt_data.get("user", {}).get("portfolios", {})
        us_portfolios = portfolios.get("us", {})

        us_file_path = ListBrokerNote.generate_path(
            account=us_portfolios.get("dw_account"),
            region=broker_note.region,
            broker_note=broker_note,
        )
        list_directories = (
            ListBrokerNote.FileRepository.list_all_directories_in_path(
                file_path=us_file_path
            )
        )
        us_files_data = ListBrokerNote.get_month_broker_notes(
            market=BrokerNoteMarket.US,
            region=BrokerNoteRegion.US,
            month_broker_notes_directories=list_directories,
        )
        return us_files_data

    @staticmethod
    def get_all_market_files_of_all_regions(jwt_data: dict, broker_note: ListBrokerNoteModel):

        portfolios = jwt_data.get("user", {}).get("portfolios", {})
        br_portfolios = portfolios.get("br", {})
        us_portfolios = portfolios.get("us", {})

        us_file_path = ListBrokerNote.generate_path(
            account=us_portfolios.get("dw_account"),
            region=BrokerNoteRegion.US,
            broker_note=broker_note,
        )
        bmf_file_path = ListBrokerNote.generate_path(
            account=br_portfolios.get("bmf_account"),
            region=BrokerNoteRegion.BR,
            broker_note=broker_note,
        )
        bovespa_file_path = ListBrokerNote.generate_path(
            account=br_portfolios.get("bovespa_account"),
            region=BrokerNoteRegion.BR,
            broker_note=broker_note,
        )

        month_broker_notes_directories = (
            ListBrokerNote.FileRepository.list_all_directories_in_path(
                file_path=bovespa_file_path
            )
        )
        bovespa_files_data = ListBrokerNote.get_month_broker_notes(
            market=BrokerNoteMarket.BOVESPA,
            region=BrokerNoteRegion.BR,
            month_broker_notes_directories=month_broker_notes_directories,
        )

        month_broker_notes_directories = (
            ListBrokerNote.FileRepository.list_all_directories_in_path(
                file_path=bmf_file_path
            )
        )
        bmf_files_data = ListBrokerNote.get_month_broker_notes(
            market=BrokerNoteMarket.BMF,
            region=BrokerNoteRegion.BR,
            month_broker_notes_directories=month_broker_notes_directories,
        )

        list_directories = (
            ListBrokerNote.FileRepository.list_all_directories_in_path(
                file_path=us_file_path
            )
        )
        us_files_data = ListBrokerNote.get_month_broker_notes(
            market=BrokerNoteMarket.BOVESPA,
            region=BrokerNoteRegion.US,
            month_broker_notes_directories=list_directories,
        )

        all_broker_note_from_all_markets = (
                us_files_data + bovespa_files_data + bmf_files_data
        )

        return all_broker_note_from_all_markets


    @staticmethod
    def get_us_market_files_data_and_us_region(jwt_data: dict, broker_note: ListBrokerNoteModel):

        portfolios = jwt_data.get("user", {}).get("portfolios", {})
        us_portfolios = portfolios.get("us", {})

        us_file_path = ListBrokerNote.generate_path(
            account=us_portfolios.get("dw_account"),
            region=BrokerNoteRegion.US,
            broker_note=broker_note,
        )
        list_directories = (
            ListBrokerNote.FileRepository.list_all_directories_in_path(
                file_path=us_file_path
            )
        )
        us_files_data = ListBrokerNote.get_month_broker_notes(
            market=BrokerNoteMarket.US,
            region=BrokerNoteRegion.US,
            month_broker_notes_directories=list_directories,
        )
        return us_files_data

    @staticmethod
    def get_all_market_files_of_br_regions(jwt_data: dict, broker_note: ListBrokerNoteModel):

        portfolios = jwt_data.get("user", {}).get("portfolios", {})
        br_portfolios = portfolios.get("br", {})

        bmf_file_path = ListBrokerNote.generate_path(
            account=br_portfolios.get("bmf_account"),
            region=BrokerNoteRegion.BR,
            broker_note=broker_note,
        )
        bovespa_file_path = ListBrokerNote.generate_path(
            account=br_portfolios.get("bovespa_account"),
            region=BrokerNoteRegion.BR,
            broker_note=broker_note,
        )

        month_broker_notes_directories = (
            ListBrokerNote.FileRepository.list_all_directories_in_path(
                file_path=bovespa_file_path
            )
        )
        bovespa_files_data = ListBrokerNote.get_month_broker_notes(
            market=BrokerNoteMarket.BOVESPA,
            region=BrokerNoteRegion.BR,
            month_broker_notes_directories=month_broker_notes_directories,
        )

        month_broker_notes_directories = (
            ListBrokerNote.FileRepository.list_all_directories_in_path(
                file_path=bmf_file_path
            )
        )
        bmf_files_data = ListBrokerNote.get_month_broker_notes(
            market=BrokerNoteMarket.BMF,
            region=BrokerNoteRegion.BR,
            month_broker_notes_directories=month_broker_notes_directories,
        )

        all_broker_note_from_all_markets = bovespa_files_data + bmf_files_data

        return all_broker_note_from_all_markets

    @staticmethod
    def get_us_market_files_of_all_regions(jwt_data: dict, broker_note: ListBrokerNoteModel):

        portfolios = jwt_data.get("user", {}).get("portfolios", {})
        us_portfolios = portfolios.get("us", {})

        us_file_path = ListBrokerNote.generate_path(
            account=us_portfolios.get("dw_account"),
            region=BrokerNoteRegion.US,
            broker_note=broker_note,
        )
        list_directories = (
            ListBrokerNote.FileRepository.list_all_directories_in_path(
                file_path=us_file_path
            )
        )
        us_file_path = ListBrokerNote.get_month_broker_notes(
            market=BrokerNoteMarket.US,
            region=BrokerNoteRegion.ALL,
            month_broker_notes_directories=list_directories,
        )
        return us_file_path

    @staticmethod
    def get_service_response(jwt_data: dict, broker_note: ListBrokerNoteModel):

        map_keys = (broker_note.market.value, broker_note.region.value)

        broker_note_response = {
            ("bovespa", "BR") : ListBrokerNote.get_bovespa_files_data_of_br_region,
            ("bmf", "BR") :  ListBrokerNote.get_bmf_files_data_of_br_region,
            ("US", "US") : ListBrokerNote.get_dw_files_data_of_us_region,
            ("ALL", "BR") : ListBrokerNote.get_all_market_files_of_br_regions,
            ("US", "ALL") : ListBrokerNote.get_us_market_files_of_all_regions,

        }.get(map_keys, [])(jwt_data=jwt_data, broker_note=broker_note)

        return broker_note_response

    @staticmethod
    def get_month_broker_notes(
        market: BrokerNoteMarket,
        region: BrokerNoteRegion,
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

                    broker_note = {
                        "market": market.value,
                        "region": region.value,
                        "day": broker_note_day,
                        "broker_note_link": broker_note_link,
                    }

                    broker_notes.append(broker_note)

                except Exception as err:
                    raise Gladsheim.error(
                        message=f"get_broker_note_file_name::directory_name:: No directory found, {err}",
                        error=err,
                    )

        broker_notes = sorted(broker_notes, key=itemgetter("day"), reverse=True)

        return broker_notes

    @classmethod
    def get_broker_note_file_name(cls, directory: dict):

        directory_name = directory.get("Key").split("/")[-1].replace(".pdf", "")
        return int(directory_name)

    @classmethod
    def generate_path(
        cls, account: str, region: BrokerNoteRegion, broker_note: ListBrokerNoteModel
    ):
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
        path = f"{account}/{region.value}/{path_route}/"
        return path
