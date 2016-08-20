# -*- coding: utf-8 -*-
import pytest
try:
    from http.client import HTTPException
except ImportError:
    from httplib import HTTPException


@pytest.fixture()
def request_good():
    """Return good request."""
    return b'GET / HTTP/1.1\r\nHOST: https://something\r\n\r\n '


@pytest.fixture()
def request_bad_method():
    """Return bad method request."""
    return b'POST / HTTP/1.1\r\nHOST: https://something\r\n\r\n '


@pytest.fixture()
def request_bad_proto():
    """Return bad proto."""
    return b'GET / HTTP/1.0\r\nHOST: https://something\r\n\r\n '


@pytest.fixture()
def request_bad_host():
    """Return invalid host."""
    return b'GET / HTTP/1.0\r\nDATE: 10:59\r\n\r\n'


def test_response_ok_parts():
    """Test response for three parts."""
    from server import response_ok
    resp_msg = response_ok()
    split = resp_msg.split(b'\r\n\r\n')
    first = split[0].split(b'\r\n')
    sections = first[0].split()
    assert len(sections) == 3


def test_response_ok_bytes():
    """Test response is bytes."""
    from server import response_ok
    resp_msg = response_ok()
    assert isinstance(resp_msg, bytes)


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


def test_parse_request_good(request_good):
    """Test that parse returns a good URI."""
    from server import parse_request
    assert parse_request(request_good) == b"/"


def test_parse_request_bad_method(request_bad_method):
    """Test parse raises proper method exception."""
    from server import parse_request, HTTPErrors
    with pytest.raises(HTTPErrors) as e:
        parse_request(request_bad_method)
    assert '405 Method not allowed.' in str(e)

def test_parse_request_bad_proto(request_bad_proto):
    """Test parse raises proper proto exception."""
    from server import parse_request, HTTPErrors
    with pytest.raises(HTTPErrors) as e:
        parse_request(request_bad_proto)
    assert '505 Version not supported.'in str(e)


def test_parse_request_good_host(request_good):
    """Test parse has host."""
    from server import parse_request
    assert parse_request(request_good) == b'/'


def test_parse_request_no_host(request_bad_host):
    from server import parse_request, HTTPErrors
    with pytest.raises(HTTPErrors) as e:
        parse_request(request_bad_host)
    assert 'Invalid Host Stuff' in str(e)
