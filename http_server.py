import socket
from dataclasses import dataclass
from utils import load_request
from request import HTTPRequest
from response import HTTPResponse


@dataclass
class HTTPServer:
    address: tuple[str, int]
    buffer: int = 1024
    server: socket = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    last_client: tuple[socket, tuple[str, int]] = ()

    def host(self):
        """Binds the server to the server address, listens for connections"""
        self.server.bind(self.address)
        self.server.listen()
        print(f"Server listening on {self.address[0]}:{self.address[1]}.\n\n")

    def receive(self) -> HTTPRequest:
        """Handles client connection, receives HTTP request from client."""
        client_socket, client_address = self.server.accept()
        self.last_client = client_socket, client_address
        print(f"HTTP request received from {client_address[0]}:{client_address[1]}.")

        request: bytes = client_socket.recv(self.buffer)

        return load_request(request)

    def send(self, response: HTTPResponse):
        """Sends back to client HTTP response that responds to the request"""
        client_socket = self.last_client[0]
        client_socket.send(response.dump())
        print(f"Successfully sent HTTP response to {self.last_client[1][0]}:{self.last_client[1][1]}.")

    def close(self):
        """Closes last client connection"""
        client_socket = self.last_client[0]
        client_socket.close()
        print(f"Closed client connection at {self.last_client[1][0]}:{self.last_client[1][1]}.\n\n")
