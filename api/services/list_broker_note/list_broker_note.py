import logging
import os

from fastapi import Query, Depends
from api.services.jwt.service import jwt_validator_and_decompile
from api.domain.enums.region import Region
from api.domain.exception.model import DataNotFoundError, NoPathFoundError

from api.repositories.files.repository import FileRepository

log = logging.getLogger()


class ListBrokerNote:
    s3_singletonv = FileRepository

    def __init__(self,
                 region: Region,
                 year: int = Query(None),
                 month: int = Query(None),
                 decompiled_jwt: dict = Depends(jwt_validator_and_decompile)
                 ):
        self.jwt = decompiled_jwt
        self.year = year
        self.month = month
        self.bovespa_account = None
        self.bmf_account = None
        self.region = region.value

    def get_account(self):
        user = self.jwt.get("user", {})
        portfolios = user.get("portfolios", {})
        br_portfolios = portfolios.get("br", {})
        self.bovespa_account = br_portfolios.get("bovespa_account")
        self.bmf_account = br_portfolios.get("bmf_account")
        self.client_id = self.jwt.get("email")

        self.bovespa_account = br_portfolios.get("user")
        self.bmf_account = br_portfolios.get("bmf_account")

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
            raise Exception(DataNotFoundError)
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
            raise Exception(NoPathFoundError)
