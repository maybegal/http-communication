# HTTP Request

class HTTPRequest:
    method: str = "GET"
    uri: str = "/"
    version: str = "HTTP/1.1"
    headers: dict[str, str] = None
    body: bytes = b""
    line_break: bytes = b"\r\n"

    def __init__(self, method: str = "GET", uri: str = "/", version: str = "HTTP/1.1", headers: dict[str, str] = None,
                 body: bytes = b"", line_break: bytes = b"\r\n"):
        self.method = method
        self.uri = uri
        self.version = version
        self.headers = headers
        self.body = body
        self.line_break = line_break

    def dump(self) -> bytes:
        """Encode HTTPRequest object into raw HTTP request bytes."""
        # Construct the request line
        request_line: bytes = f"{self.method} {self.uri} {self.version}".encode() + self.line_break

        encoded_headers: bytes = b""

        for key, value in self.headers.items():
            header: str = f"{key}: {value}"
            encoded_headers += header.encode() + self.line_break

        return request_line + encoded_headers + self.body
