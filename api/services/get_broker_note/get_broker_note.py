from fastapi import Header
from heimdall_client.bifrost import Heimdall
import logging

log = logging.getLogger()


class GetBrokerNote:

    s3_singleton: None

    def __init__(self,
                 year: str,
                 month: str,
                 day: str,
                 x_thebs_answer: str = Header(...),
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
        broker_note = GetBrokerNote.s3_singleton.generate_file_link(file_path=file_path)
        return broker_note

    def generate_path(self):
        path = f"{self.cpf}/broker_note/{self.year}/{self.month}/{self.day}.pdf"
        return path
