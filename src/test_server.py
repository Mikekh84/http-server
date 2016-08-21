# -*- coding: utf-8 -*-
import pytest


def test_response_ok_parts(request_good):
    """Test response for three parts."""
    from server import response_ok
    resp_msg = response_ok(request_good)
    split = resp_msg.split(b'\r\n\r\n')
    first = split[0].split(b'\r\n')
    sections = first[0].split()
    assert len(sections) == 3


def test_response_ok_bytes(request_good):
    """Test response is bytes."""
    from server import response_ok
    resp_msg = response_ok(request_good)
    assert isinstance(resp_msg, bytes)


def test_response_ok_part1(request_good):
    """Test response for part 1, protocol."""
    from server import response_ok
    resp_msg = response_ok(request_good)
    split = resp_msg.split()
    assert split[0] == b"HTTP/1.1"


def test_response_ok_part2(request_good):
    """Test response for part 2, status code."""
    from server import response_ok
    resp_msg = response_ok(request_good)
    split = resp_msg.split()
    assert split[1] == b"200"


def test_response_ok_part3(request_good):
    """Test response for part 3, explanation."""
    from server import response_ok
    resp_msg = response_ok(request_good)
    split = resp_msg.split()
    assert split[2] == b"OK"


def test_response_error_bytes(request_bad_proto):
    """Test response to be a byte."""
    from server import response_error
    resp_msg = response_error(request_bad_proto)
    assert isinstance(resp_msg, bytes)


def test_parse_request_good(request_good):
    """Test that parse returns a good URI."""
    from server import parse_request
    assert parse_request(request_good) == "/"


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
    assert parse_request(request_good) == '/'


def test_parse_request_no_host(request_bad_host):
    """Test Parase has no host."""
    from server import parse_request, HTTPErrors
    with pytest.raises(HTTPErrors) as e:
        parse_request(request_bad_host)
    assert '400 Bad Request' in str(e)


def test_resolve_raise_400(bad_uri):
    """Test file is returned."""
    from server import resolve_uri, HTTPErrors
    with pytest.raises(HTTPErrors) as e:
        resolve_uri(bad_uri)
    assert "404 Not Found." in str(e)


def test_resolve_uri_is_file(sample_file):
    from server import resolve_uri
    assert resolve_uri("/sample.txt") == sample_file
