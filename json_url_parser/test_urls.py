import pytest
from json_url_parser import JsonUrlParser as json_url_parser


valid_scheme = "http"
valid_scheme_secure = "https"
valid_domain_name = "www.duckduckgo.com"
valid_path = "name/of/path"
valid_port = 12345
valid_user_name = "user"
valid_password = "pass"
valid_fragment = "fragment"
valid_querykey1 = "querykey1"
valid_queryvalue1 = "queryvalue1"
valid_querykey2 = "querykey2"
valid_queryvalue2 = "queryvalue2"
valid_domain_name_ip_single_digit_in_octets = "2.1.1.2"
valid_domain_name_ip_all_digits_in_octets = "122.213.123.222"


def return_url(scheme=valid_scheme, domain_name=valid_domain_name, path=valid_path,
               port=valid_port, user_name=valid_user_name, password=valid_password,
               fragment=valid_fragment,
               querykey1=valid_querykey1, queryvalue1=valid_queryvalue1,
               querykey2=valid_querykey2, queryvalue2=valid_queryvalue2):

    url = f"{scheme}://{user_name}:{password}@{domain_name}:{port}/{path}?\
{querykey1}={queryvalue1}&{querykey2}={queryvalue2}#{fragment}"

    return url


def return_json_url(scheme=valid_scheme, domain_name=valid_domain_name, path=valid_path,
                    port=valid_port, user_name=valid_user_name, password=valid_password,
                    fragment=valid_fragment,
                    querykey1=valid_querykey1, queryvalue1=valid_queryvalue1,
                    querykey2=valid_querykey2, queryvalue2=valid_queryvalue2):

    json_url = f'[{{"scheme": "{scheme}", "domain_name": "{domain_name}", \
"path": "{path}", "port": {port}, "user_name": "{user_name}", \
"password": "{password}", "fragment": "{fragment}", \
"query": {{"{querykey1}": "{queryvalue1}", "{querykey2}": "{queryvalue2}"}}}}]'

    return json_url


valid_url_default = return_json_url()
valid_url_secure = return_json_url(scheme=valid_scheme_secure)
valid_url_ip_single_digit_in_octets = return_json_url(
    domain_name=valid_domain_name_ip_single_digit_in_octets)
valid_url_ip_all_digits_in_octets = return_json_url(
    domain_name=valid_domain_name_ip_all_digits_in_octets)

no_scheme = return_json_url(scheme="")
wrong_scheme_less_letters = return_json_url(scheme=valid_scheme[:-1])
wrong_scheme_excessive_letter = return_json_url(
    scheme=valid_scheme_secure + "s")
wrong_scheme_space_before = return_json_url(scheme=" " + valid_scheme)
wrong_scheme_excessive_colon = return_json_url(scheme=valid_scheme + ":")

wrong_domain_name = return_json_url(
    domain_name=valid_domain_name.replace(".", ""))
wrong_domain_name_dot_after_tld = return_json_url(
    domain_name=valid_domain_name + ".")
wrong_domain_name_dot_after_host_name = return_json_url(
    domain_name=str(valid_domain_name.split(".")[1:]) + ".")
wrong_ip_domain_name_1st_octet_excessive_digit = return_json_url(
    domain_name="2222.2.22.222")
wrong_ip_domain_name_last_octet_excessive_digit = return_json_url(
    domain_name="123.2.22.2222")
wrong_ip_domain_name_missing_1st_octet_with_dot = return_json_url(
    domain_name=".22.123.2")
wrong_ip_domain_name_missing_octet_without_dot = return_json_url(
    domain_name="212.2.22")
wrong_ip_domain_name_missing_last_octet_with_dot = return_json_url(
    domain_name="12.2.222.")
wrong_ip_domain_name_missing_1st_last_octets_with_dots = return_json_url(
    domain_name=".2.22.111.")

empty_query_key = return_json_url(querykey1="")
empty_query_value = return_json_url(queryvalue2="")
empty_query_key_value = return_json_url(querykey1="", queryvalue2="")
empty_query_key_value_both = return_json_url(querykey1="", queryvalue1="")

valid_url_response = "Valid URL"
not_valid_url_response = "Not valid URL"


@pytest.mark.parametrize("valid_url",
                         [valid_url_default,
                          valid_url_secure,
                          valid_url_ip_single_digit_in_octets,
                          valid_url_ip_all_digits_in_octets,
                          no_scheme])
def test_valid_url_response(valid_url):
    for header in json_url_parser(valid_url).assem_urls():
        assert valid_url_response in header


@pytest.mark.parametrize("not_valid_url",
                         [wrong_scheme_less_letters,
                          wrong_scheme_excessive_letter,
                          wrong_scheme_space_before,
                          wrong_scheme_excessive_colon,
                          wrong_domain_name,
                          wrong_domain_name_dot_after_tld,
                          wrong_domain_name_dot_after_host_name,
                          wrong_ip_domain_name_1st_octet_excessive_digit,
                          wrong_ip_domain_name_last_octet_excessive_digit,
                          wrong_ip_domain_name_missing_1st_octet_with_dot,
                          wrong_ip_domain_name_missing_octet_without_dot,
                          wrong_ip_domain_name_missing_last_octet_with_dot,
                          wrong_ip_domain_name_missing_1st_last_octets_with_dots,
                          empty_query_key,
                          empty_query_value,
                          empty_query_key_value,
                          empty_query_key_value_both])
def test_return_not_valid_url(not_valid_url):
    for header in json_url_parser(not_valid_url).assem_urls():
        assert not_valid_url_response in header
