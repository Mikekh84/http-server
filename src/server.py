import socket
from http.client import HTTPException


def parse_request(request):
    """Parse request and if valid return URI."""
    first_line = request.split()

    method, uri, proto = first_line[:3]
    if not method == b'GET':
        raise HTTPException('405 Method not allowed.')
    if not proto == b'HTTP/1.1':
        raise HTTPException('505 Version not supported.')
    return uri


def response_ok():
    """Return a well formed HTTP "200 OK" response."""
    return b"HTTP/1.1 200 OK\r\n"


def response_error():
    """Return a well formed HTTP "500 Internal Server Error" response."""
    return b"HTTP/1.1 500 Internal-Server-Error\r\n"


def server():
    """Create a running echo server."""
    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_TCP)
    address = ('127.0.0.1', 5002)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(address)
    server.listen(1)
    while True:
        conn, addr = server.accept()
        buffer_length = 8
        message_complete = False
        full_msg = ""
        while not message_complete:
            part = conn.recv(buffer_length)
            full_msg += part.decode('utf8')
            if len(part) < buffer_length:
                message_complete = True
        print(full_msg)
        conn.send(response_ok())
        conn.close()

if __name__ == '__main__':
    server()
