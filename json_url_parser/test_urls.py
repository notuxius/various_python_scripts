import pytest
from json_url_parser import JsonUrlParser as json_url_parser


valid_scheme = "http"
valid_scheme_secure = "https"
valid_domain_name = "www.google.com"
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

valid_url_response_default = f"{valid_scheme}://{valid_user_name}:{valid_password}@\
{valid_domain_name}:{valid_port}/{valid_path}?{valid_querykey1}={valid_queryvalue1}&\
{valid_querykey2}={valid_queryvalue2}#{valid_fragment}"

valid_url_response_secure = f"{valid_scheme_secure}://{valid_user_name}:{valid_password}\
@{valid_domain_name}:{valid_port}/{valid_path}?{valid_querykey1}={valid_queryvalue1}&\
{valid_querykey2}={valid_queryvalue2}#{valid_fragment}"

valid_url_response_ip_single_digit_in_octets = f"{valid_scheme}://{valid_user_name}:\
{valid_password}@{valid_domain_name_ip_single_digit_in_octets}:{valid_port}/{valid_path}?\
{valid_querykey1}={valid_queryvalue1}&{valid_querykey2}={valid_queryvalue2}#{valid_fragment}"

valid_url_response_ip_all_digits_in_octets = f"{valid_scheme}://{valid_user_name}:\
{valid_password}@{valid_domain_name_ip_all_digits_in_octets}:{valid_port}/{valid_path}?\
{valid_querykey1}={valid_queryvalue1}&{valid_querykey2}={valid_queryvalue2}#{valid_fragment}"

not_valid_url_response = "Not valid URL"


def return_url(scheme=valid_scheme, domain_name=valid_domain_name, path=valid_path,
               port=valid_port, user_name=valid_user_name, password=valid_password,
               fragment=valid_fragment,
               querykey1=valid_querykey1, queryvalue1=valid_queryvalue1,
               querykey2=valid_querykey2, queryvalue2=valid_queryvalue2):

    url = f'[{{"scheme": "{scheme}", "domain_name": "{domain_name}", \
"path": "{path}", "port": {port}, "user_name": "{user_name}", \
"password": "{password}", "fragment": "{fragment}", \
"query": {{"{querykey1}": "{queryvalue1}", "{querykey2}": "{queryvalue2}"}}}}]'

    return url


valid_url_default = return_url()
valid_url_secure = return_url(scheme=valid_scheme_secure)
valid_url_ip_single_digit_in_octets = return_url(
    domain_name=valid_domain_name_ip_single_digit_in_octets)
valid_url_ip_all_digits_in_octets = return_url(
    domain_name=valid_domain_name_ip_all_digits_in_octets)
no_scheme = return_url(scheme="")
wrong_domain_name = return_url(domain_name=valid_domain_name.replace(".", ""))
wrong_domain_name_dot_after_tld = return_url(domain_name=valid_domain_name + ".")
wrong_domain_name_dot_after_host_name = return_url(domain_name=str(valid_domain_name.split(".")[1:]) + ".")
wrong_scheme_less_letters = return_url(scheme=valid_scheme[:-1])
wrong_scheme_excessive_letter = return_url(scheme=valid_scheme_secure + "s")
wrong_scheme_space_before = return_url(scheme=" " + valid_scheme)
wrong_scheme_excessive_colon = return_url(scheme=valid_scheme + ":")
empty_query_key = return_url(querykey1="")
empty_query_value = return_url(queryvalue2="")
empty_query_key_value = return_url(querykey1="", queryvalue2="")
empty_query_key_value_both = return_url(querykey1="", queryvalue1="")


wrong_ip_domain_name_1st_octet_excessive_digit = return_url(
    domain_name="2222.2.22.222")
wrong_ip_domain_name_last_octet_excessive_digit = return_url(
    domain_name="123.2.22.2222")
wrong_ip_domain_name_missing_1st_octet_with_dot = return_url(
    domain_name=".22.123.2")
wrong_ip_domain_name_missing_octet_without_dot = return_url(
    domain_name="212.2.22")
wrong_ip_domain_name_missing_last_octet_with_dot = return_url(
    domain_name="12.2.222.")
wrong_ip_domain_name_missing_1st_last_octets_with_dots = return_url(
    domain_name=".2.22.111.")


@pytest.mark.parametrize("valid_url, valid_url_resp",
                         [(valid_url_default, valid_url_response_default),
                          (valid_url_secure, valid_url_response_secure),
                          (valid_url_ip_single_digit_in_octets,
                           valid_url_response_ip_single_digit_in_octets),
                          (valid_url_ip_all_digits_in_octets,
                           valid_url_response_ip_all_digits_in_octets),
                          (no_scheme, valid_url_response_default)])
def test_valid_url_response(valid_url, valid_url_resp):
    assert "".join(json_url_parser(
        valid_url).assem_urls()) == valid_url_resp, "Valid URL"


@pytest.mark.parametrize("not_valid_url, not_valid_url_resp",
                         [(wrong_domain_name, not_valid_url_response),
                          (wrong_domain_name_dot_after_tld, not_valid_url_response),
                          (wrong_domain_name_dot_after_host_name, not_valid_url_response),
                          (empty_query_key, not_valid_url_response),
                          (empty_query_value, not_valid_url_response),
                          (empty_query_key_value, not_valid_url_response),
                          (empty_query_key_value_both, not_valid_url_response),
                          (wrong_scheme_less_letters, not_valid_url_response),
                          (wrong_scheme_excessive_letter, not_valid_url_response),
                          (wrong_scheme_space_before, not_valid_url_response),
                          (wrong_scheme_excessive_colon, not_valid_url_response),
                          (wrong_ip_domain_name_1st_octet_excessive_digit,
                           not_valid_url_response),
                          (wrong_ip_domain_name_last_octet_excessive_digit,
                           not_valid_url_response),
                          (wrong_ip_domain_name_missing_1st_octet_with_dot,
                           not_valid_url_response),
                          (wrong_ip_domain_name_missing_octet_without_dot,
                           not_valid_url_response),
                          (wrong_ip_domain_name_missing_last_octet_with_dot,
                           not_valid_url_response),
                          (wrong_ip_domain_name_missing_1st_last_octets_with_dots,
                           not_valid_url_response)])
def test_return_not_valid_url(not_valid_url, not_valid_url_resp):
    assert "".join(json_url_parser(
        not_valid_url).assem_urls()) == not_valid_url_resp, not_valid_url_response
