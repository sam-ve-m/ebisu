# Ebisu
from src.domain.exceptions.base_exceptions.exceptions import DomainException
from src.domain.enums.response.internal_code import InternalCode

# Standards
from http import HTTPStatus


class ClosedForexOperations(DomainException):
    def __init__(self, *args, **kwargs):
        self.msg = "Opening hours for currency exchange operations are from 9:00 am to 4:30 pm."
        self.status_code = HTTPStatus.BAD_REQUEST
        self.internal_code = InternalCode.INVALID_PARAMS
        self.success = False
        super().__init__(self.msg, self.status_code, self.internal_code, self.success, args, kwargs)


class DataNotFoundInToken(DomainException):
    def __init__(self, *args, **kwargs):
        self.msg = "Error when trying to get some value in proposal token"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.DATA_VALIDATION_ERROR
        self.success = False
        super().__init__(self.msg, self.status_code, self.internal_code, self.success, args, kwargs)


class ErrorGettingValueByExchangeHash(DomainException):
    def __init__(self, *args, **kwargs):
        self.msg = "Error when trying to get some value by exchange hash"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.DATA_VALIDATION_ERROR
        self.success = False
        super().__init__(self.msg, self.status_code, self.internal_code, self.success, args, kwargs)


class DataNotFoundInJwt(DomainException):
    def __init__(self, *args, **kwargs):
        self.msg = "Error when trying to get some value in jwt_data"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.DATA_VALIDATION_ERROR
        self.success = False
        super().__init__(self.msg, self.status_code, self.internal_code, self.success, args, kwargs)


class ErrorValidatingSimulationProposalData(DomainException):
    def __init__(self, *args, **kwargs):
        self.msg = "Error when trying to validate the customer exchange simulation proposal"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.DATA_VALIDATION_ERROR
        self.success = False
        super().__init__(self.msg, self.status_code, self.internal_code, self.success, args, kwargs)


class InvalidOperation(DomainException):
    def __init__(self, *args, **kwargs):
        self.msg = "Invalid combination of base currency to quote currency"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.NOT_IMPLEMENTED
        self.success = False
        super().__init__(self.msg, self.status_code, self.internal_code, self.success, args, kwargs)


class InvalidRedisHashCombination(DomainException):
    def __init__(self, *args, **kwargs):
        self.msg = "Invalid combination to create a redis hash to find balance values"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.NOT_IMPLEMENTED
        self.success = False
        super().__init__(self.msg, self.status_code, self.internal_code, self.success, args, kwargs)


class OperationNotImplemented(DomainException):
    def __init__(self, *args, **kwargs):
        self.msg = "Nature of quote operation not implemented"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.NOT_IMPLEMENTED
        self.success = False
        super().__init__(self.msg, self.status_code, self.internal_code, self.success, args, kwargs)


class SpreadTaxNotFound(DomainException):
    def __init__(self, *args, **kwargs):
        self.msg = "Spread data not found on customer"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.DATA_NOT_FOUND
        self.success = False
        super().__init__(self.msg, self.status_code, self.internal_code, self.success, args, kwargs)
