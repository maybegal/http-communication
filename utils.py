# utils.py

from request import HTTPRequest
from response import HTTPResponse


def load_request(request: bytes, line_break: bytes = b"\r\n") -> HTTPRequest:
    """Parses raw HTTP request bytes into an HTTPRequest object."""
    # Split request bytes to lines by the line break
    lines: list[bytes] = request.split(line_break)

    # Split and decode the request line by spaces
    request_line: str = lines[0].decode()
    method, uri, version = request_line.split(" ")

    # Decode headers
    headers: dict[str, str] = {}

    for line in lines[1:]:
        if line == b"":  # Blank line signals end of headers
            break

        # Decode and split each line
        key, value = line.decode().split(": ", 1)
        # Add to headers
        headers[key] = value

    # Decode body
    body_start_index = lines.index(b"") + 1
    if body_start_index < len(lines):
        body: bytes = line_break.join(lines[body_start_index:])
    else:
        body: bytes = b""

    return HTTPRequest(method, uri, version, headers, body, line_break)


def load_response(response: bytes, line_break: bytes = b"\r\n"):
    """Parses raw HTTP response bytes into an HTTPResponse object."""
    lines: list[bytes] = response.split(line_break)

    # Split and decode the response line by spaces
    response_line: str = lines[0].decode()
    version, status, message = response_line.split(" ")

    # Decode headers
    headers: dict[str, str] = {}

    for line in lines[1:]:
        if line == b"":  # Blank line signals end of headers
            break

        # Decode and split each line
        key, value = line.decode().split(": ", 1)
        # Add to headers
        headers[key] = value

    # Decode body
    body_start_index = lines.index(b"") + 1
    if body_start_index < len(lines):
        body: bytes = line_break.join(lines[body_start_index:])
    else:
        body: bytes = b""

    return HTTPResponse(version, status, message, headers, body, line_break)