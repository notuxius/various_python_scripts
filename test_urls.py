import pytest
from json_url_parser import JsonUrlParser


@pytest.fixture
def valid_url():
    return "".join(JsonUrlParser("""[
        {
            "scheme": "http",
            "domain_name": "www.google.com",
            "path": "path",
            "port": 777,
            "username": "user",
            "password": "pass",
            "fragment": "fragment",
            "query": {
                "querykey1": "queryvalue1",
                "querykey2": "queryvalue2"
                }
        }]""").assem_urls())


@pytest.fixture
def not_valid_url():
    return "".join(JsonUrlParser("""[
        {
            "scheme": "http",
            "domain_name": "wwwgooglecom",
            "path": "path",
            "port": 777,
            "username": "user",
            "password": "pass",
            "fragment": "fragment",
            "query": {
                "querykey1": "queryvalue1",
                "querykey2": "queryvalue2"
                }
        }]""").assem_urls())


def test_valid_url(valid_url):
    assert valid_url == "http://user:pass@www.google.com:777/path?querykey1=queryvalue1&querykey2=queryvalue2#fragment"


def test_not_valid_url(not_valid_url):
    assert not_valid_url == "Not valid URL"
