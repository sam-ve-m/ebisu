import logging

from fastapi import Header, Depends
from heimdall_client.bifrost import Heimdall

from api.application_dependencies.jwt_validator import jwt_validator_and_decompile
from api.domain.enums.region import Region

log = logging.getLogger()


class GetBrokerNote:
    s3_singleton: None

    def __init__(self,
                 region: Region,
                 year: str,
                 month: str,
                 day: str,
                 decompiled_jwt: str = Depends(jwt_validator_and_decompile),
                 ):
        self.jwt = decompiled_jwt
        self.year = year
        self.month = month
        self.day = day
        self.region = region.value
        self.bovespa_account = None
        self.bmf_account = None
        self.client_id = None

    def get_account(self):
        self.bovespa_account = self.jwt.get("bovespa_account")
        self.bmf_account = self.jwt.get("bmf_account")
        self.client_id = self.jwt.get("email")

    def get_service_response(self):
        self.get_account()
        file_path = self.generate_path()
        broker_note = GetBrokerNote.s3_singleton.generate_file_link(file_path=file_path)
        return {"pdf_link": broker_note}

    def generate_path(self):
        path = f"{self.client_id}/{self.region}/broker_note/{self.year}/{self.month}/{self.day}.pdf"
        return path
