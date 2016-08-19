import socket
try:
    from http.client import HTTPException
except ImportError:
    from httplib import HTTPException


def parse_request(request):
    """Parse request and if valid return URI."""
    split_req = request.split(b'\r\n', 1)
    method, uri, proto = split_req[0].split()
    headers = split_req[1].split(b'\r\n\r\n')
    split_headers = headers[0].split(b'\r\n')
    header_details = [items.split(b':', 1) for items in split_headers]
    header_dict = {k: v for k, v in header_details}
    if b'HOST' not in header_dict:
            raise HTTPException('No HOST In Header')
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
