# server.py

import json

from response import HTTPResponse
from request import HTTPRequest
from endpoint import HTTPEndpoint
from server_host import HTTPServer

portfolio = {}


def respond(http_request: HTTPRequest, endpoints: list[HTTPEndpoint]) -> HTTPResponse:
    """
    Handles an HTTPRequest by locating the server-side action specified in the request's URI.
    Executes the action from the server's collection of actions and returns its result as an HTTPResponse.
    """
    uri_matched = False

    for endpoint in endpoints:
        if http_request.uri == endpoint.uri:
            uri_matched = True

            if http_request.method == endpoint.method:
                try:
                    return endpoint.endpoint(http_request)
                except ValueError as e:
                    print(f"ValueError in endpoint: {e}")

                    return HTTPResponse(
                        status=504,
                        message="Internal Server Error"
                    )
                except KeyError as e:
                    print(f"KeyError in endpoint: {e}")
                    return HTTPResponse(
                        status=504,
                        message="Internal Server Error"
                    )

    if not uri_matched:
        return HTTPResponse(
            status=404,
            message="Not Found",
        )

    return HTTPResponse(
        status=405,
        message="Method Not Allowed",
    )


def get_portfolio(request: HTTPRequest) -> HTTPResponse:
    body = json.dumps(portfolio)

    return HTTPResponse(
        headers={
            "Content-Length": str(len(body)),
            "Content-Type": "application/json",
            "Connection": "Keep-Alive"
        },
        body=body.encode()
    )


def post_stock(request: HTTPRequest) -> HTTPResponse:
    stocks: dict = json.loads(request.body)

    for stock, amount in stocks.items():
        portfolio[stock] = amount

    return HTTPResponse()


def main() -> None:
    """Hosts a server to communicate with a client through receiving HTTP request and sending HTTP response."""
    server = HTTPServer(("127.0.0.1", 8000))

    endpoints = [
        HTTPEndpoint("/portfolio", "GET", get_portfolio),
        HTTPEndpoint("/portfolio", "POST", post_stock),
    ]

    server.host()

    while True:
        try:
            request: HTTPRequest = server.receive()
            response: HTTPResponse = respond(request, endpoints)
            server.send(response)

            if request.headers.get("Connection", "").lower() != "keep-alive":
                break

        except Exception as e:
            print(f"Server error: {e}")
            break

    server.close()


if __name__ == '__main__':
    main()
