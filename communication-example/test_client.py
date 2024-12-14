# test_client.py

import json
import socket

from request import HTTPRequest
from response import HTTPResponse
from utils import load_response


def request(address: tuple[str, int], data: HTTPRequest, buffer: int = 1024) -> HTTPResponse:
    """Sends HTTP request to given server and data through TCP connection, returns HTTP response."""
    client = socket.socket()
    client.connect(address)

    # Send HTTP request to the server
    client.send(data.dump())
    print(f"Successfully sent HTTP request to server at {address[0]}:{address[1]}.")

    # Receive HTTP response from the server
    response: bytes = client.recv(buffer)

    return load_response(response)


def main() -> None:
    """Example connection to a server, communicates through sending HTTP request and receiving HTTP response."""
    try:
        address = ("127.0.0.1", 5000)

        portfolio = {
            "NVDA": 500,
            "PLTR": 250,
            "TSMC": 320,
            "BTCUSD": 800,
        }

        body = json.dumps(portfolio)

        http_request = HTTPRequest(
            method="POST",
            uri="/portfolio",
            version="HTTP/1.1",
            headers={
                "Host": "127.0.0.1",
                "User-Agent": "TCP/1.0",
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Content-Length": str(len(body)),
                "Connection": "Keep-Alive",
                "Keep-Alive": "timeout=5, max=100",
            },
            body=body.encode(),
        )

        response = request(address, http_request)
        print(f"Received HTTP response:\n\033[92m{response}\033[39;49m\n")

        http_request = HTTPRequest(
            method="GET",
            uri="/portfolio",
            version="HTTP/1.1",
            headers={
                "Host": "127.0.0.1",
                "User-Agent": "TCP/1.0",
                "Accept": "application/json",
                "Connection": "Close",
            },
        )

        response = request(address, http_request)
        print(f"Received HTTP response:\n\033[92m{response}\033[39;49m\n")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    main()
