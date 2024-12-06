# server.py


from response import HTTPResponse
from request import HTTPRequest
from endpoint import HTTPEndpoint
from server_host import HTTPServer, close


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


def get_home(request: HTTPRequest) -> HTTPResponse:
    body = f"<html><body><h1>Home page</h1><h2>{request.body}</h2><p>{request.version}</p></body></html>"

    return HTTPResponse(
        headers={
            "Content-Length": str(len(body)),
            "Content-Type": "text/html",
            "Connection": "Closed"
        },
        body=body.encode()
    )


def get_pricing(request: HTTPRequest) -> HTTPResponse:
    body = f"<html><body><h1>Pricing page</h1><h2>{request.body}</h2><p>{request.version}</p></body></html>"

    return HTTPResponse(
        headers={
            "Content-Length": str(len(body)),
            "Content-Type": "text/html",
            "Connection": "Closed"
        },
        body=body.encode()
    )


def main() -> None:
    """Hosts a server to communicate with a client through receiving HTTP request and sending HTTP response."""
    server = HTTPServer(("127.0.0.1", 3000))
    endpoints = [
        HTTPEndpoint("/home", "GET", get_home),
        HTTPEndpoint("/pricing", "GET", get_pricing)
    ]

    server.host()

    while True:
        request, client = server.receive()
        response, client = respond(request, endpoints)
        close(response, client)


if __name__ == '__main__':
    main()
