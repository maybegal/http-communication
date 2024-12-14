# test_client.py

import json
import socket

from request import HTTPRequest
from response import HTTPResponse
from utils import load_response


def send_request(address: tuple[str, int], data: HTTPRequest, buffer: int = 1024) -> HTTPResponse:
    """Sends HTTP request to given server and data through TCP connection, returns HTTP response."""
    client = socket.socket()
    client.connect(address)

    # Send HTTP request to the server
    client.send(data.dump())
    print(f"Sent HTTP request:\n\033[94m{data}\033[39;49m\n")

    # Receive HTTP response from the server
    response = load_response(client.recv(buffer))

    print(f"Received HTTP response:\n\033[92m{response}\033[39;49m\n")
    return response


def main() -> None:
    """Example connection to a server, communicates through sending HTTP request and receiving HTTP response."""
    address = ("127.0.0.1", 5000)

    # Post new portfolio
    portfolio = {
        "NVDA": 14,
        "PLTR": 28,
        "TSMC": 2,
        "TSLA": 24,
        "NNE": 23,
    }

    request = HTTPRequest(
        method="POST",
        uri="/portfolio",
        body=json.dumps(portfolio).encode(),
    )

    response = send_request(address, request)

    # Get portfolio
    request = HTTPRequest(
        method="GET",
        uri="/portfolio",
    )

    response = send_request(address, request)

    # Update the portfolio
    update_stocks = {
        "PLTR": 47,
        "TSMC": 1,
    }

    request = HTTPRequest(
        method="PUT",
        uri="/portfolio",
        body=json.dumps(update_stocks).encode()
    )

    response = send_request(address, request)

    # Remove stocks from portfolio
    remove_stocks = ["NNE"]

    request = HTTPRequest(
        method="DELETE",
        uri="/portfolio",
        body=json.dumps(remove_stocks).encode()
    )

    response = send_request(address, request)

    # Get portfolio
    request = HTTPRequest(
        method="GET",
        uri="/portfolio",
    )

    response = send_request(address, request)


if __name__ == '__main__':
    main()
