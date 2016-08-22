# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pytest


MSG_TABLE = [
    ('hello', 'hello'),
    ('hello' * 10, 'hello' * 10),
    ('12345678', '12345678')
    ('helloéöĉ', 'helloéöĉ')
]


@pytest.mark.parametrize('msg, result', MSG_TABLE)
def test_client_send(msg, result):
    """Test that echo server is functioning."""
    from client import client
    assert client(msg) == result
