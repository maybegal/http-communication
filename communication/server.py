# server.py

import socket

from response import HTTPResponse
from request import HTTPRequest
from endpoint import HTTPEndpoint
from server_host import HTTPServer


def respond(endpoints: list[HTTPEndpoint], http_request: HTTPRequest) -> HTTPResponse:
    """
    Handles an HTTPRequest by locating the server-side action specified in the request's URI.
    Executes the action from the server's collection of actions and returns its result as an HTTPResponse.
    """
    pass


def get_home(request: HTTPRequest) -> HTTPResponse:
    body = "<html><body><h1>Home page</h1></body></html>"

    return HTTPResponse(
        headers={
            "Content-Length": str(len(body)),
            "Content-Type": "text/html",
            "Connection": "Closed"
        },
        body=body.encode()
    )


def get_pricing(request: HTTPRequest) -> HTTPResponse:
    body = "<html><body><h1>Home page</h1></body></html>"

    return HTTPResponse(
        headers={
            "Content-Length": str(len(body)),
            "Content-Type": "text/html",
            "Connection": "Closed"
        },
        body=body.encode()
    )


def main() -> None:
    """Hosts a server to communicate with a client through receiving HTTP request and sending HTTP response."""
    # Start a TCP server to listen for client connections
    server = HTTPServer(("127.0.0.1", 3000))

    endpoints = [
        HTTPEndpoint("/home", "GET", get_home),
        HTTPEndpoint("/pricing", "GET", get_pricing)
    ]


if __name__ == '__main__':
    main()
