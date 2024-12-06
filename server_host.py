import socket
from dataclasses import dataclass
from utils import load_request
from request import HTTPRequest
from response import HTTPResponse


@dataclass
class HTTPServer:
    address: tuple[str, int]
    buffer: int = 1024
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def host(self):
        """Binds the server to the server address, listens for connections"""
        self.server.bind(self.address)
        self.server.listen()
        print(f"Server listening on {self.address[0]}:{self.address[1]}.\n")

    def receive(self) -> tuple[HTTPRequest, socket]:
        """Handles client connection, receives HTTP request from client."""
        client, client_address = self.server.accept()
        print(f"HTTP request received from {client_address[0]}:{client_address[1]}.")
        request: bytes = client.recv(self.buffer)

        return load_request(request), client


def close(response: HTTPResponse, client: socket):
    """Sends back to client HTTP response that responds to the request, closes connection."""
    client.send(response.dump())
    print(f"Successfully sent HTTP response.\n")

    # Close connection
    client.close()
