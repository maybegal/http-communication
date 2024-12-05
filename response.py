# HTTP Response

from dataclasses import dataclass, field


@dataclass
class HTTPResponse:
    """Represents an HTTP response, including version, status, headers, and body."""
    version: str = "HTTP/1.1"
    status: int = 200
    message: str = "OK"
    headers: dict[str, str] = field(default_factory=dict)
    body: bytes = b""
    line_break: bytes = b"\r\n"

    def dump(self) -> bytes:
        """
        Serializes the HTTPResponse into raw HTTP bytes.

        Returns:
            bytes: The raw HTTP response.
        """
        # Build the response line
        response_line: bytes = f"{self.version} {self.status} {self.message}".encode() + self.line_break

        # Format headers as "Key: Value\r\n"
        encoded_headers: bytes = b""
        for key, value in self.headers.items():
            header: str = f"{key}: {value}"
            encoded_headers += header.encode() + self.line_break

        # Return the response line, headers, a blank line, boy
        return response_line + encoded_headers + self.line_break + self.body
