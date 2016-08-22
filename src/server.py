from __future__ import unicode_literals
import socket
import os
import io
from email.utils import formatdate

class HTTPErrors(Exception):
    """HTTP Error exception class."""

    def __init__(self, message):
        """Intialize Error with message."""
        self.message = message


def resolve_uri(uri):
    """Resolve uri and return body for response."""
    root = os.path.abspath("./webroot")
    path = root + uri
    content_type = u""
    if os.path.isfile(path):
        with io.open(path, 'rb') as file:
            content = file.read()
        file.close()
        if uri.endswith('txt'):
            content_type = u"text"
        elif uri.endswith('html'):
            content_type = u"HTML"
        elif uri.endswith(('png', 'jpg', 'jpeg')):
            content_type = u"image"
        return (content, content_type)
    if os.path.isdir(path):
        dir_list = [
            "<li>" + file + "</li>" for file in os.listdir(path)
        ]
        joined = "".join(dir_list).strip(',')
        content_type = "directory"
        content = "<!DOCTYPE html><h1>{}</h1>{}".format(uri, joined)
        return content.encode('utf8'), content_type
    else:
        raise HTTPErrors('404 Not Found.')


def parse_request(request):
    """Parse request and if valid return URI."""
    # import pdb; pdb.set_trace()
    split_req = request.split('\r\n', 1)
    method, uri, proto = split_req[0].split()
    headers = split_req[1].split('\r\n\r\n', 1)
    split_headers = headers[0].split('\r\n')
    header_details = [items.split(':', 1) for items in split_headers]
    header_dict = {k.upper(): v.strip() for k, v in header_details}
    if 'HOST' not in header_dict:
        raise HTTPErrors('400 Bad Request.')
    if not method == 'GET':
        raise HTTPErrors('405 Method not allowed.')
    if not proto == 'HTTP/1.1':
        raise HTTPErrors('505 Version not supported.')
    return uri


def response_ok(content, content_type):
    """Return a well formed HTTP "200 OK" response."""
    response = "HTTP/1.1 200 OK\r\nContent-Type:{}\r\nContent-Length:{}\r\nDate:{}\r\n\r\n".format(
        content_type,
        len(content),
        formatdate(usegmt=True),
    )
    return response.encode('utf8') + content


def response_error(message):
    """Return an error code and message.."""
    response = "HTTP/1.1{}\r\n\r\n <h1>{}</h1>".format(message, message)
    return response.encode('utf8')


def server():
    """Create a running echo server."""
    try:
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
            buffer_length = 64
            message_complete = False
            request = ""
            while not message_complete:
                part = conn.recv(buffer_length)
                request += part.decode('utf8')
                if len(part) < buffer_length:
                    message_complete = True
            print(request)
            try:
                parsed = parse_request(request)
                resolved = resolve_uri(parsed)
            except HTTPErrors as e:
                response = response_error(e)
            else:
                response = response_ok(resolved[0], resolved[1])
            conn.sendall(response)
            conn.close()
    except KeyboardInterrupt:
        pass
        server.close()
if __name__ == '__main__':
    server()
