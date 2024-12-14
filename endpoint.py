# HTTP Endpoint

from typing import Callable
from request import HTTPRequest
from response import HTTPResponse
from dataclasses import dataclass


@dataclass
class HTTPEndpoint:
    """Represents an HTTP endpoint, including uri, method, endpoint function."""
    uri: str
    method: str
    endpoint: Callable[[HTTPRequest], HTTPResponse]
