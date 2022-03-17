import logging

from fastapi import Depends

from api.application_dependencies.jwt_validator import jwt_validator_and_decompile
from api.domain.enums.region import Region
from api.exceptions.exceptions import NoPath, NotFoundError

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
        user = self.jwt.get("user", {})
        portfolios = user.get("portfolios", {})
        br_portfolios = portfolios.get("br", {})
        self.bovespa_account = br_portfolios.get("bovespa_account")
        self.bmf_account = br_portfolios.get("bmf_account")
        self.client_id = self.jwt.get("email")

    def get_service_response(self):
        self.get_account()
        file_path = self.generate_path()
        broker_note = GetBrokerNote.s3_singleton.generate_file_link(file_path=file_path)
        data = {"pdf_link": broker_note}
        if not data:
            raise NotFoundError({"pdf_link": "BROKER NOTE NOT FOUND"})
        return data

    def generate_path(self):
        path = f"{self.bmf_account}/{self.region}/broker_note/{self.year}/{self.month}/{self.day}.pdf"
        if self.bmf_account and self.region and self.year and self.month and self.day in path:
            return path
        raise NoPath("NoPathError: No Path Error")
