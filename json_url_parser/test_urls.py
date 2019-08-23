import pytest
from json_url_parser import JsonUrlParser as json_url_parser


# TODO use format()?
valid_url_all_fields = """[{
    "scheme": "http",
    "domain_name": "www.google.com",
    "path": "name/of/path",
    "port": 777,
    "username": "user",
    "password": "pass",
    "fragment": "fragment",
    "query": {
        "querykey1": "queryvalue1",
        "querykey2": "queryvalue2"
        }
}]"""

not_valid_url_wrong_domain_name = """[{
    "scheme": "http",
    "domain_name": "wwwgooglecom",
    "path": "name/of/path",
    "port": 777,
    "username": "user",
    "password": "pass",
    "fragment": "fragment",
    "query": {
        "key1": "value1",
        "key2": "value2"
        }
}]"""

not_valid_url_empty_query_value = """[{
    "scheme": "http",
    "domain_name": "www.google.com",
    "path": "name/of/path",
    "port": 777,
    "username": "user",
    "password": "pass",
    "fragment": "fragment",
    "query": {
        "key1": "",
        "key2": ""
        }
}]"""

not_valid_url_wrong_scheme = """[{
    "scheme": "httpss",
    "domain_name": "www.google.com",
    "path": "name/of/path",
    "port": 777,
    "username": "user",
    "password": "pass",
    "fragment": "fragment",
    "query": {
        "key1": "",
        "key2": ""
        }
}]"""

valid_url_response = "http://user:pass@www.google.com:777/name/of/path\
?querykey1=queryvalue1&querykey2=queryvalue2#fragment"
not_valid_url_response = 'Not valid URL'

@pytest.mark.parametrize("valid_url, valid_url_resp",
                         [(valid_url_all_fields, valid_url_response)])
def test_valid_url_response(valid_url, valid_url_resp):
    assert "".join(json_url_parser(
        valid_url).assem_urls()) == valid_url_resp, "Valid URL"


@pytest.mark.parametrize("not_valid_url, not_valid_url_resp",
                         [(not_valid_url_wrong_domain_name, not_valid_url_response),
                          (not_valid_url_empty_query_value, not_valid_url_response),
                          (not_valid_url_wrong_scheme, not_valid_url_response)])
def test_return_not_valid_url(not_valid_url, not_valid_url_resp):
    assert "".join(json_url_parser(
        not_valid_url).assem_urls()) == not_valid_url_resp, "Not valid URL"
