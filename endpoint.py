# HTTP Endpoint

from typing import Callable
from request import HTTPRequest
from response import HTTPResponse
from dataclasses import dataclass


@dataclass
class HTTPEndpoint:
    uri: str
    method: str
    endpoint: Callable[[HTTPRequest], HTTPResponse]
