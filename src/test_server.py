# -*- coding: utf-8 -*-


def test_response_ok_parts():
    """Test response for three parts."""
    from server import response_ok
    resp_msg = response_ok()
    split = resp_msg.split()
    assert len(split) == 3


def test_response_ok_bytes():
    """Test response is bytes."""
    from server import response_ok
    resp_msg = response_ok()
    assert type(resp_msg) == type(b" ")


def test_response_ok_part1():
    """Test response for part 1, protocol."""
    from server import response_ok
    resp_msg = response_ok()
    split = resp_msg.split()
    assert split[0] == b"HTTP/1.1"


def test_response_ok_part2():
    """Test response for part 2, status code."""
    from server import response_ok
    resp_msg = response_ok()
    split = resp_msg.split()
    assert split[1] == b"200"


def test_response_ok_part3():
    """Test response for part 3, explanation."""
    from server import response_ok
    resp_msg = response_ok()
    split = resp_msg.split()
    assert split[2] == b"OK"


def test_response_error_bytes():
    """Test response to be a byte."""
    from server import response_error
    resp_msg = response_error()
    assert isinstance(resp_msg, bytes)


def test_response_error_parts():
    """Test response has 3 parts for error."""
    from server import response_error
    resp_msg = response_error()
    assert len(resp_msg.split()) == 3


def test_response_error_part1():
    """Test response for part 1, protocol."""
    from server import response_error
    resp_msg = response_error()
    split = resp_msg.split()
    assert split[0] == b"HTTP/1.1"


def test_response_error_part2():
    """Test response for part 2, status code."""
    from server import response_error
    resp_msg = response_error()
    split = resp_msg.split()
    assert split[1] == b"500"


def test_response_error_part3():
    """Test response for part 3, explanation."""
    from server import response_error
    resp_msg = response_error()
    split = resp_msg.split()
    assert split[2] == b"Internal-Server-Error"
