# -*- coding: utf-8 -*-


import pytest


MSG_TABLE = [
    (u'hello'),
    (u'hello' * 10),
    (u'12345678')
]


@pytest.mark.parametrize('msg', MSG_TABLE)
def test_client_send(msg):
    """Test that echo server is functioning."""
    from client import client_send
    assert client_send(msg) == msg
