from enum import Enum


class HTTPMethod(Enum):
    """
    HTTP Method Enum Class

    Enum containing the various valid HTTP methods.

    Attributes:


    """

    CONNECT = "CONNECT"
    DELETE = "DELETE"
    GET = "GET"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    PATCH = "PATCH"
    POST = "POST"
    PUT = "PUT"
    TRACE = "TRACE"
