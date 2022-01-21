import os

from fastapi import Header, Query
from heimdall_client.bifrost import Heimdall
import logging

log = logging.getLogger()


class ListBrokerNote:

    s3_singleton: None

    def __init__(self,
                 x_thebs_answer: str = Header(...),
                 year: int = Query(None),
                 month: int = Query(None),
                 day: int = Query(None),
                 ):
        self.jwt = x_thebs_answer
        self.year = year
        self.month = month
        self.day = day
        self.bovespa_account = None
        self.bmf_account = None
        self.cpf = None

    def get_account(self):
        heimdall = Heimdall(logger=log)
        jwt_data = heimdall.decrypt_payload(jwt=self.jwt)
        self.bovespa_account = jwt_data.get("bovespa_account")
        self.bmf_account = jwt_data.get("bmf_account")
        self.cpf = jwt_data.get("email")

    def get_service_response(self):
        self.get_account()
        file_path = self.generate_path()

        list_directories = ListBrokerNote.s3_singleton.list_all_directories_in_path(file_path=file_path)
        directories = []

        if list_directories.get('CommonPrefixes'):
            directories = [ListBrokerNote.get_directory_name(directory) for directory in
                           list_directories.get('CommonPrefixes')]

        return directories

    @staticmethod
    def get_directory_name(directory: dict):
        directory_name = ""
        if directory:
            directory_name = directory.get('Prefix').split('/')[-2]

        return directory_name

    def generate_path(self):
        path_route = os.path.join(*tuple(str(path_fragment)
                                         for path_fragment in ('broker_note', self.year, self.month, self.day)
                                         if path_fragment is not None))
        path = f"{self.cpf}/{path_route}/"

        return path

