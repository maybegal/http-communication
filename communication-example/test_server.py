# test_server.py

import json

from response import HTTPResponse
from request import HTTPRequest
from endpoint import HTTPEndpoint
from server import HTTPServer


# Portfolio is a dictionary where each key represents a stock ticker (string),
# and the corresponding value represents the quantity of shares owned.
portfolio: dict[str, int] = {}


def get_portfolio(request: HTTPRequest) -> HTTPResponse:
    """Handles GET requests to retrieve the current portfolio."""
    return HTTPResponse(
        body=json.dumps(portfolio).encode()
    )


def post_stock(request: HTTPRequest) -> HTTPResponse:
    """Handles POST requests to add new stocks to the portfolio."""
    try:
        stocks: dict[str, int] = json.loads(request.body)
        portfolio.update(stocks)
        for ticker, quantity in stocks.items():
            print(f"{quantity} {ticker} stocks added to portfolio.")
        return HTTPResponse()
    except json.JSONDecodeError:
        return HTTPResponse(status=400, message="Invalid JSON format")


def update_stocks(request: HTTPRequest) -> HTTPResponse:
    """Handles PUT requests to update stock quantities in the portfolio."""
    try:
        stocks: dict[str, int] = json.loads(request.body)
        for ticker, quantity in stocks.items():
            if ticker in portfolio:
                portfolio[ticker] = quantity
                print(f"{ticker} stock quantity updated to {quantity}.")
        return HTTPResponse()
    except json.JSONDecodeError:
        return HTTPResponse(status=400, message="Invalid JSON format")


def delete_stocks(request: HTTPRequest) -> HTTPResponse:
    """Handles DELETE requests to remove stocks from the portfolio."""
    try:
        tickers: list[str] = json.loads(request.body)
        for ticker in tickers:
            portfolio.pop(ticker, None)
            print(f"{ticker} stock removed from portfolio.")
        return HTTPResponse()
    except json.JSONDecodeError:
        return HTTPResponse(status=400, message="Invalid JSON format")


def main() -> None:
    """Hosts a server to communicate with a client through receiving HTTP request and sending HTTP response."""
    endpoints = [
        HTTPEndpoint("/portfolio", "GET", get_portfolio),
        HTTPEndpoint("/portfolio", "POST", post_stock),
        HTTPEndpoint("/portfolio", "PUT", update_stocks),
        HTTPEndpoint("/portfolio", "DELETE", delete_stocks)
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
