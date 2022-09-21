from etria_logger import Gladsheim

from src.domain.exceptions import FailToGetDataFromTransportLayer


class DwBaseTransport:
    @staticmethod
    def _handle_http_error_from_drive_wealth_request(request: any, response: any):
        if response.status != 200:
            Gladsheim.error(
                message=f"DwBaseTransport::execute_get::Http error when request dw api",
                response=response,
                request=request,
            )
            raise FailToGetDataFromTransportLayer()

    @staticmethod
    def _handle_dw_error_status_from_response(request: any, response: dict):
        if isinstance(response, dict) and response.get("errorCode"):
            Gladsheim.error(
                message=f"DwBaseTransport::execute_get::Dw error code when request dw api",
                response=response,
                request=request,
            )
            raise FailToGetDataFromTransportLayer()
