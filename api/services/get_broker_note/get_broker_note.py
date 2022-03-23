import logging

from fastapi import Depends

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
                 decompiled_jwt: dict = Depends(jwt_validator_and_decompile),
                 ):
        self.jwt: dict = decompiled_jwt
        self.year = year
        self.month = month
        self.day = day
        self.region = region.value
        self.bovespa_account = None
        self.bmf_account = None

    def get_account(self):
        user = self.jwt.get("user", {})
        portfolios = user.get("portfolios", {})
        br_portfolios = portfolios.get("br", {})

        self.bovespa_account = br_portfolios.get("user")
        self.bmf_account = br_portfolios.get("bmf_account")

    def get_service_response(self):
        self.get_account()
        file_path = self.generate_path()
        broker_note = GetBrokerNote.s3_singleton.generate_file_link(file_path=file_path)
        return {"pdf_link": broker_note}

    def generate_path(self):
        path = f"{self.bmf_account}/{self.region}/broker_note/{self.year}/{self.month}/{self.day}.pdf"
        return path
