# Ebisu
from src.domain.exceptions.base_exceptions.exceptions import DomainException
from src.domain.enums.response.internal_code import InternalCode

# Standards
from http import HTTPStatus


class InvalidOperation(DomainException):
    def __init__(self, *args, **kwargs):
        self.msg = "Invalid combination of base currency to quote currency"
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


class OperationNotImplemented(DomainException):
    def __init__(self, *args, **kwargs):
        self.msg = "Nature of quote operation not implemented"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.NOT_IMPLEMENTED
        self.success = False
        super().__init__(self.msg, self.status_code, self.internal_code, self.success, args, kwargs)


class ErrorOnValidateExchangeSimulationProposalData(DomainException):
    def __init__(self, *args, **kwargs):
        self.msg = "Error when trying to validate the customer exchange simulation proposal"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.DATA_VALIDATION_ERROR
        self.success = False
        super().__init__(self.msg, self.status_code, self.internal_code, self.success, args, kwargs)
