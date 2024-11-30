# client.py

import socket

from request import HTTPRequest


IP = "127.0.0.1"
PORT = 3002
ADDRESS = (IP, PORT)
BUFFER = 4096


def main() -> None:
    """Connects to a server and communicates through sending HTTP request and receiving HTTP response."""
    try:
        # Establish TCP connection
        client = socket.socket()
        client.connect(ADDRESS)

        http_request = HTTPRequest(
            method="GET",
            uri="/home",
            version="HTTP/1.1",
            headers={
                "Host": "127.0.0.1",
                "User-Agent": "TCP/1.0",
                "Accept": "text/html",
                "Content-Type": "text/html"
            },
            body="<html><body><h1>Hey!</h1></body></html>".encode(),
        )

        # Send HTTP request to the server
        client.send(http_request.dump())
        print(f"Successfully sent HTTP request to server at {ADDRESS[0]}:{ADDRESS[1]}.")

        # Receive HTTP response from the server
        response: bytes = client.recv(BUFFER)
        print(f"Received HTTP response:\n\033[92m{response.decode()}\033[39;49m\n")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    main()
