# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import socket


def server():
    """Receive a client's message, echo message back."""
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    address = ('127.0.0.1', 5000)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(address)
    server.listen(1)
    print('server running')
    try:
        while True:
            conn, addr = server.accept()
            buffer_length = 8
            message_complete = False
            full_msg = b""
        while not message_complete:
            part = conn.recv(buffer_length)
            full_msg += part.decode
            if len(part) < buffer_length:
                message_complete = True
        print(full_msg.decode('utf8'))
        conn.sendall(full_msg)
        conn.close()
    except KeyboardInterrupt:
        server.close


if __name__ == '__main__':
    server()
