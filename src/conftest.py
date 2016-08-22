import pytest
import io


@pytest.fixture()
def request_good():
    """Return good request."""
    return b'GET / HTTP/1.1\r\nHOST: https://something\r\n\r\n '


@pytest.fixture()
def request_bad_method():
    """Return bad method request."""
    return 'POST / HTTP/1.1\r\nHOST: https://something\r\n\r\n '


@pytest.fixture()
def request_bad_proto():
    """Return bad proto."""
    return 'GET / HTTP/1.0\r\nHOST: https://something\r\n\r\n '


@pytest.fixture()
def request_bad_host():
    """Return invalid host."""
    return 'GET / HTTP/1.0\r\nDATE: 10:59\r\n\r\n'


@pytest.fixture()
def bad_uri():
    """Return a bad uri."""
    return ';slkdfs;'


@pytest.fixture()
def sample_file():
    """Sample text."""
    file = io.open("webroot/sample.txt")
    content = file.read()
    file.close()
    return (content.encode('utf8'), 'text')


@pytest.fixture()
def parse_good():
    """Request for parse."""
    return 'GET / HTTP/1.1 \r\nHOST: something\r\n\r\n some text.'


# @pytest.fixure()
# def sample_dir():
#     """Sample dir."""
#     return '<h1>/</h1><li>make_time.py</li><li>a_web_page.html'
#     '</li><li>sample.txt</li><li>images</li>'
