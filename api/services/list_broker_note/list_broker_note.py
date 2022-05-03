import os
from operator import itemgetter
from typing import List

from api.domain.validators.exchange_info.list_broker_note_validator import ListBrokerNoteModel, BrokerNoteMarket, \
    BrokerNoteRegion
from api.repositories.files.repository import FileRepository


class ListBrokerNote:
    FileRepository = FileRepository

    @classmethod
    def get_service_response(cls, jwt_data: dict, broker_note: ListBrokerNoteModel):
        user = jwt_data.get("user", {})
        portfolios = user.get("portfolios", {})
        br_portfolios = portfolios.get("br", {})
        us_portfolios = portfolios.get("us", {})

        if broker_note.market == BrokerNoteMarket.BOVESPA:
            bovespa_file_path = cls.generate_path(account=br_portfolios.get("bovespa_account"), region=broker_note.region, broker_note=broker_note)
            month_broker_notes_directories = ListBrokerNote.FileRepository.list_all_directories_in_path(
                file_path=bovespa_file_path
            )
            bovespa_files_data = cls.get_month_broker_notes(
                market=BrokerNoteMarket.BOVESPA,
                region=broker_note.region,
                month_broker_notes_directories=month_broker_notes_directories
            )
            return bovespa_files_data

        if broker_note.market == BrokerNoteMarket.BMF:
            bmf_file_path = cls.generate_path(account=br_portfolios.get("bmf_account"), region=broker_note.region, broker_note=broker_note)
            month_broker_notes_directories = ListBrokerNote.FileRepository.list_all_directories_in_path(
                file_path=bmf_file_path
            )
            bmf_files_data = cls.get_month_broker_notes(
                market=BrokerNoteMarket.BOVESPA,
                region=broker_note.region,
                month_broker_notes_directories=month_broker_notes_directories
            )
            return bmf_files_data

        if broker_note.market == BrokerNoteMarket.US:
            us_file_path = cls.generate_path(account=us_portfolios.get("dw_id"), region=broker_note.region, broker_note=broker_note)
            list_directories = ListBrokerNote.FileRepository.list_all_directories_in_path(
                file_path=us_file_path
            )
            us_files_data = cls.get_month_broker_notes(
                market=BrokerNoteMarket.BOVESPA,
                region=broker_note.region,
                month_broker_notes_directories=list_directories
            )
            return us_files_data

        if broker_note.market == BrokerNoteMarket.ALL and broker_note.region == BrokerNoteRegion.ALL:
            us_file_path = cls.generate_path(account=us_portfolios.get("dw_id"), region=BrokerNoteRegion.US, broker_note=broker_note)
            bmf_file_path = cls.generate_path(account=br_portfolios.get("bmf_account"), region=BrokerNoteRegion.BR, broker_note=broker_note)
            bovespa_file_path = cls.generate_path(account=br_portfolios.get("bovespa_account"), region=BrokerNoteRegion.BR, broker_note=broker_note)

            month_broker_notes_directories = ListBrokerNote.FileRepository.list_all_directories_in_path(
                file_path=bovespa_file_path
            )
            bovespa_files_data = cls.get_month_broker_notes(
                market=BrokerNoteMarket.BOVESPA,
                region=broker_note.region,
                month_broker_notes_directories=month_broker_notes_directories
            )

            month_broker_notes_directories = ListBrokerNote.FileRepository.list_all_directories_in_path(
                file_path=bmf_file_path
            )
            bmf_files_data = cls.get_month_broker_notes(
                market=BrokerNoteMarket.BMF,
                region=broker_note.region,
                month_broker_notes_directories=month_broker_notes_directories
            )

            list_directories = ListBrokerNote.FileRepository.list_all_directories_in_path(
                file_path=us_file_path
            )
            us_files_data = cls.get_month_broker_notes(
                market=BrokerNoteMarket.BOVESPA,
                region=broker_note.region,
                month_broker_notes_directories=list_directories
            )

            all_broker_note_from_all_markets = us_files_data + bovespa_files_data + bmf_files_data

            return all_broker_note_from_all_markets

        if broker_note.market == BrokerNoteMarket.ALL and broker_note.region == BrokerNoteRegion.BR:
            bmf_file_path = cls.generate_path(account=br_portfolios.get("bmf_account"), region=BrokerNoteRegion.BR, broker_note=broker_note)
            bovespa_file_path = cls.generate_path(account=br_portfolios.get("bovespa_account"), region=BrokerNoteRegion.BR, broker_note=broker_note)

            month_broker_notes_directories = ListBrokerNote.FileRepository.list_all_directories_in_path(
                file_path=bovespa_file_path
            )
            bovespa_files_data = cls.get_month_broker_notes(
                market=BrokerNoteMarket.BOVESPA,
                region=broker_note.region,
                month_broker_notes_directories=month_broker_notes_directories
            )

            month_broker_notes_directories = ListBrokerNote.FileRepository.list_all_directories_in_path(
                file_path=bmf_file_path
            )
            bmf_files_data = cls.get_month_broker_notes(
                market=BrokerNoteMarket.BMF,
                region=broker_note.region,
                month_broker_notes_directories=month_broker_notes_directories
            )

            all_broker_note_from_all_markets = bovespa_files_data + bmf_files_data

            return all_broker_note_from_all_markets

        if broker_note.market == BrokerNoteMarket.US and broker_note.region == BrokerNoteRegion.ALL:
            us_file_path = cls.generate_path(account=us_portfolios.get("dw_id"), region=BrokerNoteRegion.US, broker_note=broker_note)
            list_directories = ListBrokerNote.FileRepository.list_all_directories_in_path(
                file_path=us_file_path
            )
            us_files_data = cls.get_month_broker_notes(
                market=BrokerNoteMarket.BOVESPA,
                region=broker_note.region,
                month_broker_notes_directories=list_directories
            )
            return us_files_data

        return []

    @staticmethod
    def get_month_broker_notes(market: BrokerNoteMarket, region: BrokerNoteRegion, month_broker_notes_directories: List[str]):

        has_month_broker_note = month_broker_notes_directories.get("Contents")
        broker_notes = []
        if has_month_broker_note:
            for directory in month_broker_notes_directories.get("Contents"):
                broker_note_day = ListBrokerNote.get_broker_note_file_name(directory)
                broker_note_link = FileRepository.generate_file_link(file_path=directory.get("Key"), url_link_expire_seconds=900)

                broker_note = {
                    "market": market.value,
                    "region": region.value,
                    "day": broker_note_day,
                    "broker_note_link": broker_note_link
                }
                broker_notes.append(broker_note)

        broker_notes = sorted(broker_notes, key=itemgetter('day'), reverse=True)

        return broker_notes

    @classmethod
    def get_broker_note_file_name(cls, directory: dict):
        directory_name = ""
        if directory:
            directory_name = directory.get("Key").split("/")[-1].replace(".pdf", "")

        return int(directory_name)

    @classmethod
    def generate_path(cls, account: str, region: BrokerNoteRegion, broker_note: ListBrokerNoteModel):
        path_route = os.path.join(
            *tuple(
                str(path_fragment)
                for path_fragment in ("broker_note", broker_note.year, broker_note.month)
                if path_fragment is not None
            )
        )
        path = f"{account}/{region.value}/{path_route}/"
        return path
