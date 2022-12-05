from src.domain.enums.response.internal_code import InternalCode
from src.domain.exceptions.base_exceptions.model import ServiceException
from http import HTTPStatus


class InvalidDeviceInfo(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "Invalid DeviceInfo"
        self.status_code = HTTPStatus.UNAUTHORIZED
        self.internal_code = InternalCode.DEVICE_INFO_INVALID
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )
