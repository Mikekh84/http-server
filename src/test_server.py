# -*- coding: utf-8 -*-


def test_response_ok_parts():
    """Test response for three parts."""
    from server import response_ok
    resp_msg = response_ok()
    assert resp_msg.split(" ") == 3


def test_response_ok_bytes():
    """Test response is bytes."""
    from server import response_ok
    resp_msg = response_ok()
    assert isinstance(resp_msg, (str, bytes))
