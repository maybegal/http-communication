import socket
from dataclasses import dataclass
from utils import load_request, load_response
from endpoint import HTTPEndpoint
from request import HTTPRequest
from response import HTTPResponse


@dataclass
class HTTPServer:
    address: tuple[str, int]
    buffer: int = 1024
    socket = socket.socket()

    def host(self):
        """Binds the server to the server address, listens for connections"""
        self.socket.bind(self.address)
        self.socket.listen()
        print(f"Server listening on {self.address[0]}:{self.address[1]}.")

    def handle(self):
        """
        Handles client connection, receives HTTP request from client.
        Sends back to client HTTP response that responds to the request, closes connection.
        """
        # Accept a new client connection
        client, client_address = self.socket.accept()

        # Receive from client
        request: bytes = client.recv(self.buffer)
        print(f"Received HTTP request:\n\033[92m{request.decode()}\033[39;49m\n")

        # Parse HTTP request
        http_request = load_request(request)

        # Generate a response
        http_response = respond(http_request)

        client.send(http_response.dump())
        print("Successfully sent back HTTP response to request.")

        # Close connection
        client.close()
        print("Connection closed.")
