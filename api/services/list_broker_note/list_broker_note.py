import os

from api.domain.enums.region import Region
from api.domain.exception.model import DataNotFoundError, NoPathFoundError
from api.repositories.files.repository import FileRepository


class ListBrokerNote:
    s3_singleton = FileRepository
    bmf_account = None

    @classmethod
    def get_service_response(cls, jwt_data: dict, region: Region, year: int, month: int):
        user = jwt_data.get("user", {})
        portfolios = user.get("portfolios", {})
        br_portfolios = portfolios.get("br", {})
        cls.bovespa_account = br_portfolios.get("bovespa_account")
        cls.bmf_account = br_portfolios.get("bmf_account")
        cls.client_id = jwt_data.get("email")

        file_path = cls.generate_path(region=region, year=year, month=month)

        list_directories = ListBrokerNote.s3_singleton.list_all_directories_in_path(
            file_path=file_path
        )
        directories = []
        files = []
        if list_directories.get("CommonPrefixes"):
            directories = [
                ListBrokerNote.get_directory_name(directory)
                for directory in list_directories.get("CommonPrefixes")
            ]

        if list_directories.get("Contents"):
            files = [
                ListBrokerNote.get_file_name(directory)
                for directory in list_directories.get("Contents")
            ]

        files_data = {
            "available": sorted(directories) if directories else sorted(files)
        }
        if not files_data:
            raise Exception(DataNotFoundError)
        return files_data

    @classmethod
    def get_directory_name(cls, directory: dict):
        directory_name = ""
        if directory:
            directory_name = directory.get("Prefix").split("/")[-2]

        return int(directory_name)

    @classmethod
    def get_file_name(cls, directory: dict):
        directory_name = ""
        if directory:
            directory_name = directory.get("Key").split("/")[-1].replace(".pdf", "")

        return int(directory_name)

    @classmethod
    def generate_path(cls, region: Region, year: int, month: int):
        path_route = os.path.join(
            *tuple(
                str(path_fragment)
                for path_fragment in ("broker_note", year, month)
                if path_fragment is not None
            )
        )
        path = f"{region.value}/{cls.bmf_account}/{path_route}/"

        if cls.bmf_account and region.value and path_route in path:
            return path
        else:
            raise Exception(NoPathFoundError)
