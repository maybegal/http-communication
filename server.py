# server.py

import socket
from response import HTTPResponse
from request import HTTPRequest
from utils import load_request, load_response

IP = "127.0.0.1"
PORT = 3000
ADDRESS = (IP, PORT)
BUFFER = 4096


def respond(http_request: HTTPRequest) -> HTTPResponse:
    """Generate a generic HTTP response based on the given HTTP request."""
    status: int = 200
    message: str = "OK"

    body: bytes = "<html><body><h1>Hello</h1></body></html>".encode()

    headers: dict[str, str] = {
        "Content-Length": str(len(body)),
        "Content-Type": "text/html",
        "Connection": "Closed"
    }

    return HTTPResponse(http_request.version, status, message, headers, body)


def main() -> None:
    """Hosts a server to communicate with a client through receiving HTTP request and sending HTTP response."""

    # Create a TCP socket
    server = socket.socket()

    # Bind to IP address and port
    server.bind(ADDRESS)

    # Listen for incoming connections
    server.listen()

    print(f"Server listening on {ADDRESS[0]}:{ADDRESS[1]}.")

    while True:
        # Accept a new client connection
        client, client_address = server.accept()

        # Receive from client
        request: bytes = client.recv(BUFFER)

        # Parse HTTP request
        http_request: HTTPRequest = load_request(request)

        # Generate a response
        http_response: HTTPResponse = respond(http_request)

        # Send HTTP response back to client
        client.send(http_response.dump())

        # Close connection
        client.close()


if __name__ == '__main__':
    main()