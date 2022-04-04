from api.domain.enums.region import Region
from api.domain.exception.model import NoPathFoundError
from api.repositories.files.repository import FileRepository


class GetBrokerNotePDF:
    bmf_account = None
    s3_singleton = FileRepository

    @classmethod
    def get_service_response(cls, region: Region, year: int, month: int, day: int, jwt_data: dict):
        user = jwt_data.get("user", {})
        portfolios = user.get("portfolios", {})
        br_portfolios = portfolios.get("br", {})
        cls.bovespa_account = br_portfolios.get("bovespa_account")
        cls.bmf_account = br_portfolios.get("bmf_account")
        cls.client_id = jwt_data.get("email")

        file_path = f"{cls.bmf_account}/{region}/broker_note/{year}/{month}/{day}.pdf"
        if (
            cls.bmf_account
            and region
            and year
            and month
            and day in file_path
        ):
            broker_note = GetBrokerNotePDF.s3_singleton.generate_file_link(file_path=file_path)
            data = {"pdf_link": broker_note}
            return data
        raise Exception(NoPathFoundError)
