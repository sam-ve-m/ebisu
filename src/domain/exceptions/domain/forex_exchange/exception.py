from src.domain.exceptions.base_exceptions.exceptions import DomainException


class InvalidOperation(DomainException):
    pass


class MissingExchangeAccountId(DomainException):
    pass


class MissingSpreadTax(DomainException):
    pass
