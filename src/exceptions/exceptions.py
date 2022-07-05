class UnauthorizedError(Exception):
    pass


class ForbiddenError(Exception):
    pass


class BadRequestError(Exception):
    pass


class InternalServerError(Exception):
    pass


class NoPath(Exception):
    pass


class NotFoundError(Exception):
    pass


class MoneyFlowResolverNoFoundError(Exception):
    pass


class InvalidAccountsOwnership(Exception):
    pass


class UnableToProcessMoneyFlow(Exception):
    pass


class NotMappedCurrency(Exception):
    pass


class InvalidElectronicaSignature(Exception):
    pass