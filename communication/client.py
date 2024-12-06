# client.py
import json
import socket

from http_request import HTTPRequest


SERVER_ADDRESS = ("127.0.0.1", 8000)
BUFFER = 1024


def main() -> None:
    """Example connection to a server, communicates through sending HTTP request and receiving HTTP response."""
    try:
        # Establish TCP connection
        client = socket.socket()
        client.connect(SERVER_ADDRESS)

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

        # Send HTTP request to the server
        client.send(http_request.dump())
        print(f"Successfully sent HTTP request to server at {SERVER_ADDRESS[0]}:{SERVER_ADDRESS[1]}.")

        # Receive HTTP response from the server
        response: bytes = client.recv(BUFFER)
        print(f"Received HTTP response:\n\033[92m{response.decode()}\033[39;49m\n")

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

        # Send HTTP request to the server
        client.send(http_request.dump())
        print(f"Successfully sent HTTP request to server at {SERVER_ADDRESS[0]}:{SERVER_ADDRESS[1]}.")

        # Receive HTTP response from the server
        response: bytes = client.recv(BUFFER)
        print(f"Received HTTP response:\n\033[92m{response.decode()}\033[39;49m\n")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    main()
