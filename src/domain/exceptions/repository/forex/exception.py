# Ebisu
from src.domain.exceptions.base_exceptions.exceptions import RepositoryException
from src.domain.enums.response.internal_code import InternalCode

# Standards
from http import HTTPStatus


class CustomerForexDataNotFound(RepositoryException):
    def __init__(self, *args, **kwargs):
        self.msg = "Customer exchange data not found"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.DATA_NOT_FOUND
        self.success = False
        super().__init__(self.msg, self.status_code, self.internal_code, self.success, *args, **kwargs)


class CustomerPersonalDataNotFound(RepositoryException):
    def __init__(self, *args, **kwargs):
        self.msg = "Not found some data in customer"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.DATA_NOT_FOUND
        self.success = False
        super().__init__(self.msg, self.status_code, self.internal_code, self.success, *args, **kwargs)


class ErrorTryingToInsertData(RepositoryException):
    def __init__(self, *args, **kwargs):
        self.msg = 'Error trying to insert exchange proposal executed data'
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.INTERNAL_SERVER_ERROR
        self.success = False
        super().__init__(self.msg, self.status_code, self.internal_code, self.success, *args, **kwargs)


class ErrorTryingToGetForexAccountNumber(RepositoryException):
    def __init__(self, *args, **kwargs):
        self.msg = 'Error trying to get forex account number'
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.DATA_NOT_FOUND
        self.success = False
        super().__init__(self.msg, self.status_code, self.internal_code, self.success, *args, **kwargs)


class ErrorTryingToGetForexClientId(RepositoryException):
    def __init__(self, *args, **kwargs):
        self.msg = 'Error trying to get forex client id'
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.DATA_NOT_FOUND
        self.success = False
        super().__init__(self.msg, self.status_code, self.internal_code, self.success, *args, **kwargs)


class ErrorTryingToGetForexAccountData(RepositoryException):
    def __init__(self, *args, **kwargs):
        self.msg = 'Error trying to get forex account data'
        self.status_code = HTTPStatus.UNAUTHORIZED
        self.internal_code = InternalCode.DATA_NOT_FOUND
        self.success = False
        super().__init__(self.msg, self.status_code, self.internal_code, self.success, *args, **kwargs)
