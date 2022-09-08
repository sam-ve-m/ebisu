# Ebisu
from src.domain.exceptions.base_exceptions.exceptions import RepositoryException

# Standards
from http import HTTPStatus


class CustomerExchangeDataNotFound(RepositoryException):
    def __init__(self, *args, **kwargs):
        self.msg = "Customer exchange data not found"
        self.code = HTTPStatus.INTERNAL_SERVER_ERROR
        super().__init__(self.msg, self.code, args, kwargs)
