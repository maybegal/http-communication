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

    def is_keep_alive(self) -> bool:
        """Determines if the HTTP request is using a keep-alive connection."""
        connection_value = self.headers.get("Connection", "")
        return connection_value == "Keep-Alive"

    def get_timeout(self) -> int:
        if self.is_keep_alive():
            keep_alive_value = self.headers.get("Keep-Alive", "")
            for param in keep_alive_value.split(", "):
                key, _, value = param.strip().partition("=")
                if key == "timeout" and value.isdigit():
                    return int(value)
        return 0

    def get_max_request(self) -> int:
        if self.is_keep_alive():
            keep_alive_value = self.headers.get("Keep-Alive", "")
            for param in keep_alive_value.split(", "):
                key, _, value = param.strip().partition("=")
                if key == "max" and value.isdigit():
                    return int(value)
        return 0
