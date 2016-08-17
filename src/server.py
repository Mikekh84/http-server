import socket


def response_ok():
    """Return a well formed HTTP "200 OK" response."""
    return b"HTTP/1.1 200 OK"

# def response_error():
    """Returns a well formed HTTP "500 Internal Server Error" response."""


def server():
    """Create a running echo server."""
    server = socket.socket(socket.AF_INET,
                                             socket.SOCK_STREAM,
                                             socket.IPPROTO_TCP
                                             )
    address = ('127.0.0.1', 5000)
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
