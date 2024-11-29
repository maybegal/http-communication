# HTTP Request

class HTTPRequest:
    method: str = "GET"
    uri: str = "/"
    version: str = "HTTP/1.1"
    headers: dict[str, str] = None
    body: bytes = b""
    line_break: bytes = b"\r\n"

    def __init__(self, method: str = "GET", uri: str = "/", version: str = "HTTP/1.1", headers: dict[str, str] = None, body: bytes = b"", line_break: bytes = b"\r\n"):
        self.method = method
        self.uri = uri
        self.version = version
        self.headers = headers
        self.body = body
        self.line_break = line_break

    def dump(self) -> bytes:
        encoded_method: bytes = self.method.encode()
        encoded_uri: bytes = self.uri.encode()
        encoded_version: bytes = self.version.encode() + self.line_break

        encoded_headers: bytes = b""

        for header_key, header_value in self.headers.items():
            header: str = header_key + ": " + header_value
            encoded_headers += header.encode() + self.line_break

        return encoded_method + encoded_uri + encoded_version + encoded_headers + self.body
