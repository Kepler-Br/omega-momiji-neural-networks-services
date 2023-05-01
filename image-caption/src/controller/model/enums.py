from enum import Enum


class ResponseStatus(str, Enum):
    OK: str = 'OK'
    NOT_READY: str = 'NOT_READY'
    BAD_REQUEST: str = 'BAD_REQUEST'
    INTERNAL_SERVER_ERROR: str = 'INTERNAL_SERVER_ERROR'
    TOO_MANY_REQUESTS: str = 'TOO_MANY_REQUESTS'
    NOT_FOUND: str = 'NOT_FOUND'
