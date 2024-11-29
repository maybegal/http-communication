# HTTP Response

class HTTPResponse:
    version: str = "HTTP/1.1"
    status: int = 200
    message: str = "OK"
    headers: dict[str, str] = None
    body: bytes = b""
    line_break: bytes = b"\r\n"

    def __init__(self, version: str = "HTTP/1.1", status: int = 200, message: str = "OK",
                 headers: dict[str, str] = None, body: bytes = b"", line_break: bytes = b"\r\n"):
        self.version = version
        self.status = status
        self.message = message
        self.headers = headers
        self.body = body
        self.line_break = line_break

    def dump(self) -> bytes:
        """Encode HTTPResponse object into raw HTTP response bytes."""
        # Construct the response line
        response_line: bytes = f"{self.version} {self.status}".encode() + self.line_break

        encoded_headers: bytes = b""

        for key, value in self.headers:
            header: str = f"{key} {value}"
            encoded_headers += header.encode() + self.line_break

        return response_line + encoded_headers + self.body
