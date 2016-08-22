# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import socket
import sys


def client(msg):
    """Send a message and return msg received by server."""
    info = socket.getaddrinfo('127.0.0.1', 5000)
    stream_info = [i for i in info if i[1] == socket.SOCK_STREAM][0]
    client = socket.socket(*stream_info[:3])
    client.connect(stream_info[-1])
    client.sendall(msg.encode('utf8'))
    client.shutdown(socket.SHUT_WR)s
    buffer_length = 8
    reply_complete = False
    full_msg = b""
    while not reply_complete:
        part = client.recv(buffer_length)
        full_msg += part
        if len(part) < buffer_length:
            reply_complete = True
            break
    print(full_msg.decode('utf8'))
    reply_complete = True
    client.close()

if __name__ == '__main__':
    print(client(sys.argv[1]))
