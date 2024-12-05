# HTTP Request

from dataclasses import dataclass, field


@dataclass
class HTTPRequest:
    """Represents an HTTP request, including method, URI, version, headers, and body."""
    method: str = "GET"
    uri: str = "/"
    version: str = "HTTP/1.1"
    headers: dict[str, str] = field(default_factory=dict)
    body: bytes = b""
    line_break: bytes = b"\r\n"

    def dump(self) -> bytes:
        """
        Serializes the HTTPRequest object into raw HTTP request bytes.

        Returns:
            bytes: The raw HTTP request in byte format.
        """
        # Construct the request line
        request_line: bytes = f"{self.method} {self.uri} {self.version}".encode() + self.line_break

        # Format headers as "Key: Value\r\n"
        encoded_headers: bytes = b""
        for key, value in self.headers.items():
            header: str = f"{key}: {value}"
            encoded_headers += header.encode() + self.line_break

        # Return request line, headers, a blank line, and body in raw bytes
        return request_line + encoded_headers + self.line_break + self.body
