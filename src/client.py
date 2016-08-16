import socket
import sys


def client_send(msg):
    """Send message and return msg received by server."""
    infos = socket.getaddrinfo('127.0.0.1', 5000)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    client = socket.socket(*stream_info[:3])
    client.connect(stream_info[-1])
    client.sendall(msg.encode('utf8'))
    buffer_length = 8
    reply_complete = False
    full_msg = ""
    while not reply_complete:
        part = client.recv(buffer_length)
        full_msg += part.decode('utf8')
        if len(part) < buffer_length:
            reply_complete = True
    client.close
    return full_msg

if __name__ == '__main__':
    print(client_send(sys.argv[1]))
