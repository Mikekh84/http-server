from __future__ import unicode_literals
import socket


class HTTPErrors(Exception):
    """HTTP Error exception class."""

    def __init__(self, message):
        """Intialize Error with message."""
        self.message = message


def parse_request(request):
    """Parse request and if valid return URI."""
    split_req = request.split('\r\n', 1)
    method, uri, proto = split_req[0].split()
    headers = split_req[1].split('\r\n\r\n')
    split_headers = headers[0].split('\r\n')
    header_details = [items.split(':', 1) for items in split_headers]
    header_dict = {k.upper(): v.strip() for k, v in header_details}
    if 'HOST' not in header_dict:
        raise HTTPErrors('400 Host Header not found.')
    if not method == 'GET':
        raise HTTPErrors('405 Method not allowed.')
    if not proto == 'HTTP/1.1':
        raise HTTPErrors('505 Version not supported.')
    return uri


def response_ok(message):
    """Return a well formed HTTP "200 OK" response."""
    response = "HTTP/1.1 200 OK\r\n\r\n{}".format(message)
    return response.encode('utf8')


def response_error(message):
    """Return a well formed HTTP  response."""
    response = "HTTP 1/1 {}\r\n\r\n{}".format(message, message)
    return response.encode('utf8')


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
        request = ""
        while not message_complete:
            part = conn.recv(buffer_length)
            request += part.decode('utf8')
            if len(part) < buffer_length:
                message_complete = True
        print(request)
        try:
            parse_request(request)
        except HTTPErrors as e:
            response = response_error(e)
        else:
            response = response_ok(request)
        conn.sendall(response)
        conn.close()

if __name__ == '__main__':
    server()
