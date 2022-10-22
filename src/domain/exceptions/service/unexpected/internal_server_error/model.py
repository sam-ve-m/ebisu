from http import HTTPStatus

from src.domain.enums.response.internal_code import InternalCode
from src.domain.exceptions.base_exceptions.model import ServiceException


class InternalServerError(ServiceException):

    def __init__(self, *args, **kwargs):
        self.msg = "Unexpected error occured"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.INTERNAL_SERVER_ERROR
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )
