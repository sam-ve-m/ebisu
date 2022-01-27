import logging
import os

from fastapi import Header, Query
from heimdall_client.bifrost import Heimdall

from api.domain.enums.region import Region

log = logging.getLogger()


class ListBrokerNote:
    s3_singleton: None

    def __init__(self,
                 region: Region,
                 x_thebs_answer: str = Header(...),
                 year: int = Query(None),
                 month: int = Query(None),
                 ):
        self.jwt = x_thebs_answer
        self.year = year
        self.month = month
        self.bovespa_account = None
        self.bmf_account = None
        self.client_id = None
        self.region = region.value

    def get_account(self):
        heimdall = Heimdall(logger=log)
        jwt_data = heimdall.decrypt_payload(jwt=self.jwt)
        self.bovespa_account = jwt_data.get("bovespa_account")
        self.bmf_account = jwt_data.get("bmf_account")
        self.client_id = jwt_data.get("email")

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

        return {"available": sorted(directories) if directories else sorted(files)}

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
        path = f"{self.client_id}/{self.region}/{path_route}/"

        return path
