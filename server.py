# HTTPServer

import socket
from dataclasses import dataclass
from utils import load_request
from request import HTTPRequest
from response import HTTPResponse
from endpoint import HTTPEndpoint


def respond(http_request: HTTPRequest, endpoints: list[HTTPEndpoint]) -> HTTPResponse:
    """
    Handles an HTTPRequest by locating the server-side action specified in the request's URI.
    Executes the action from the server's collection of actions and returns its result as an HTTPResponse.
    """
    uri_matched = False

    for endpoint in endpoints:
        if http_request.uri == endpoint.uri:
            uri_matched = True

            if http_request.method == endpoint.method:
                try:
                    return endpoint.endpoint(http_request)
                except ValueError as e:
                    print(f"ValueError in endpoint: {e}")

                    return HTTPResponse(
                        status=504,
                        message="Internal Server Error"
                    )
                except KeyError as e:
                    print(f"KeyError in endpoint: {e}")
                    return HTTPResponse(
                        status=504,
                        message="Internal Server Error"
                    )

    if not uri_matched:
        return HTTPResponse(
            status=404,
            message="Not Found",
        )

    return HTTPResponse(
        status=405,
        message="Method Not Allowed",
    )


@dataclass
class HTTPServer:
    endpoints: list[HTTPEndpoint]
    headers: dict[str, str] = None
    server: socket.socket = None

    def host(self, address: tuple[str, int]):
        """Hosts new server, binds the server to the server address, listens for connections."""
        self.server = socket.socket()
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server.bind(address)

        self.server.listen()
        print(f"Server listening on {address[0]}:{address[1]}.\n")

    def handle(self, close: bool = True, client: socket.socket = None, buffer: int = 1024):
        """Handles client connection. Receives message from client, responds to the request through the connection."""
        # If no client was given, try to accept new client connection
        if client is None:
            client = self.server.accept()

        # Receive request from client
        request: bytes = client.recv(buffer)
        print(f"HTTP request received from .")
        http_request: HTTPRequest = load_request(request)

        # Respond to HTTPRequest
        http_response: HTTPResponse = respond(http_request, self.endpoints)
        client.send(http_response.dump())
        print(f"Successfully sent HTTP response to .")

        if close:
            client.close()
            print(f"Closed client connection at .\n\n")
