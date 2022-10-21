from http import HTTPStatus

from src.domain.enums.response.internal_code import InternalCode
from src.domain.exceptions.base_exceptions.model import ServiceException


class FailToSaveAuditingTrail(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "Fail to save auditing trail"
        self.status_code = HTTPStatus.SERVICE_UNAVAILABLE
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
