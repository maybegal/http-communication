# server.py

import socket

from response import HTTPResponse
from request import HTTPRequest
from utils import load_request


IP = "127.0.0.1"
PORT = 3000
ADDRESS = (IP, PORT)
BUFFER = 4096


def respond(http_request: HTTPRequest) -> HTTPResponse:
    """Generate a generic HTTP response based on the given HTTP request."""
    body = "<html><body><h1>Hello</h1></body></html>"

    return HTTPResponse(
        version=http_request.version,
        status=200,
        message="OK",
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
    server = socket.socket()
    server.bind(ADDRESS)
    server.listen()

    print(f"Server listening on {ADDRESS[0]}:{ADDRESS[1]}.")

    while True:
        try:
            # Accept a new client connection
            client, client_address = server.accept()

            # Receive from client
            request: bytes = client.recv(BUFFER)
            print(f"Received HTTP request:\n\033[92m{request.decode()}\033[39;49m\n")

            # Parse HTTP request
            http_request: HTTPRequest = load_request(request)

            # Generate a response
            http_response: HTTPResponse = respond(http_request)

            # Send HTTP response back to client
            encoded_response = http_response.dump()

            client.send(encoded_response)
            print("Successfully sent back HTTP response to request.")

            # Close connection
            client.close()
            print("Connection closed.")

        except Exception as e:
            print(f"Error handling client connection: {e}")


if __name__ == '__main__':
    main()
