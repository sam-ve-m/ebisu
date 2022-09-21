# Ebisu
from src.domain.exceptions.base_exceptions.exceptions import RepositoryException
from src.domain.enums.response.internal_code import InternalCode

# Standards
from http import HTTPStatus


class CustomerExchangeDataNotFound(RepositoryException):
    def __init__(self, *args, **kwargs):
        self.msg = "Customer exchange data not found"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.DATA_NOT_FOUND
        self.success = False
        super().__init__(self.msg, self.status_code, self.internal_code, self.success, args, kwargs)
