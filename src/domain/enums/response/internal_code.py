# Standards
from enum import IntEnum


class InternalCode(IntEnum):
    SUCCESS = 0
    INVALID_PARAMS = 10
    JWT_INVALID = 30
    NOT_IMPLEMENTED = 90
    DATA_VALIDATION_ERROR = 97
    DATA_ALREADY_EXISTS = 98
    DATA_NOT_FOUND = 99
    INTERNAL_SERVER_ERROR = 100
    DROPPED_TOKEN = 200
    EXPIRED_TOKEN = 201
    ERROR_IN_CARONTE = 300

    def __repr__(self):
        return self.value
