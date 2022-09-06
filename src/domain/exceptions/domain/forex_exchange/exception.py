from src.domain.exceptions.base_exceptions.exceptions import DomainException


class InvalidOperation(DomainException):
    pass


class SpreadTaxNotFound(DomainException):
    pass


class OperationNotImplemented(DomainException):
    pass

