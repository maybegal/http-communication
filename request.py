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
        pass
