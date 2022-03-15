import logging
import os

from fastapi import Query, Depends
from api.application_dependencies.jwt_validator import jwt_validator_and_decompile
from api.domain.enums.region import Region
from api.exceptions.exceptions import NoPath, NotFoundError


log = logging.getLogger()


class ListBrokerNote:
    s3_singleton: None

    def __init__(self,
                 region: Region,
                 year: int = Query(None),
                 month: int = Query(None),
                 decompiled_jwt: str = Depends(jwt_validator_and_decompile)
                 ):
        self.jwt = decompiled_jwt
        self.year = year
        self.month = month
        self.bovespa_account = None
        self.bmf_account = None
        self.client_id = None
        self.region = region.value

    def get_account(self):
        self.bovespa_account = self.jwt.get("bovespa_account")
        self.bmf_account = self.jwt.get("bmf_account")
        self.client_id = self.jwt.get("email")

    def get_service_response(self):
        self.get_account()
        file_path = self.generate_path()

        list_directories = ListBrokerNote.s3_singleton.list_all_directories_in_path(file_path=file_path)
        directories = []
        files = []
        if list_directories.get('CommonPrefixes'):
            directories = [ListBrokerNote.get_directory_name(directory) for directory in
                           list_directories.get('CommonPrefixes')]

        if list_directories.get('Contents'):
            files = [ListBrokerNote.get_file_name(directory) for directory in
                     list_directories.get('Contents')]

        files_data = {"available": sorted(directories) if directories else sorted(files)}
        if not files_data:
            raise NotFoundError("NotFoundError: The Data was not Found")
        return files_data

    @staticmethod
    def get_directory_name(directory: dict):
        directory_name = ""
        if directory:
            directory_name = directory.get('Prefix').split('/')[-2]

        return int(directory_name)

    @staticmethod
    def get_file_name(directory: dict):
        directory_name = ""
        if directory:
            directory_name = directory.get('Key').split('/')[-1].replace('.pdf', '')

        return int(directory_name)

    def generate_path(self):
        path_route = os.path.join(*tuple(str(path_fragment)
                                         for path_fragment in ('broker_note', self.year, self.month)
                                         if path_fragment is not None))
        path = f"{self.bmf_account}/{self.region}/{path_route}/"

        if self.bmf_account and self.region and path_route in path:
            return path
        else:
            raise NoPath("No Path Error: Path Not Found")
