# test_server.py

import json

from response import HTTPResponse
from request import HTTPRequest
from endpoint import HTTPEndpoint
from server import HTTPServer


portfolio = {}


def get_portfolio(request: HTTPRequest) -> HTTPResponse:
    body = json.dumps(portfolio)

    return HTTPResponse(
        headers={
            "Content-Length": str(len(body)),
            "Content-Type": "application/json"
        },
        body=body.encode()
    )


def post_stock(request: HTTPRequest) -> HTTPResponse:
    try:
        stocks: dict = json.loads(request.body)
        for stock, amount in stocks.items():
            portfolio[stock] = amount

        print(f"Portfolio updated: {portfolio}")
        return HTTPResponse()

    except json.JSONDecodeError:
        return HTTPResponse(
            status=422,
            message="Unprocessable Entity"
        )


def main() -> None:
    """Hosts a server to communicate with a client through receiving HTTP request and sending HTTP response."""
    endpoints = [
        HTTPEndpoint("/portfolio", "GET", get_portfolio),
        HTTPEndpoint("/portfolio", "POST", post_stock),
    ]

    server = HTTPServer(endpoints)
    server.host(("127.0.0.1", 5000))

    while True:
        try:
            server.handle()

        except Exception as e:
            print(f"Server error: {e}")


if __name__ == '__main__':
    main()
