from api.domain.exception.model import NoPathFoundError
from api.domain.validators.exchange_info_validators.get_broker_note_validator import GetBrokerNoteModel
from api.repositories.files.repository import FileRepository


class GetBrokerNotePDF:
    bmf_account = None
    s3_singleton = FileRepository

    @classmethod
    def get_service_response(cls, broker_note_pdf: GetBrokerNoteModel, jwt_data: dict):
        user = jwt_data.get("user", {})
        portfolios = user.get("portfolios", {})
        br_portfolios = portfolios.get("br", {})
        cls.bovespa_account = br_portfolios.get("bovespa_account")
        cls.bmf_account = br_portfolios.get("bmf_account")
        cls.client_id = jwt_data.get("email")

        file_path = f"{cls.bmf_account}/{broker_note_pdf.region}/broker_note/{broker_note_pdf.year}/{broker_note_pdf.month}/{broker_note_pdf.day}.pdf "

        if (
            cls.bmf_account
            and broker_note_pdf.region
            and broker_note_pdf.year
            and broker_note_pdf.month
            and broker_note_pdf.day
        ):
            broker_note = GetBrokerNotePDF.s3_singleton.generate_file_link(
                file_path=file_path
            )
            data = {"pdf_link": broker_note}
            return data
        raise Exception(NoPathFoundError)
