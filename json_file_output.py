#!/usr/bin/env python
from json import loads as json_loads
from json.decoder import JSONDecodeError
from sys import stderr as sys_stderr
from sys import exit as sys_exit
from sys import argv as sys_argv
from re import sub as re_sub
from re import compile as re_compile
from re import match as re_match
from re import IGNORECASE as re_ignore_case


def print_error(error):
    if isinstance(error, dict):
        sys_stderr.write(str(error) + "\n\n")

    else:
        sys_stderr.write("ERROR: " + str(error) + "\n")


def print_info(info):
    if isinstance(info, dict):
        print(str(info))

    else:
        print("INFO:", str(info))


def item_is_present(item, input_json_object):
    return bool(item in input_json_object and input_json_object[item])


try:
    with open(sys_argv[1]) as json_file:
        json_file_contents = json_loads(json_file.read())

except JSONDecodeError:
    print_error("Bad JSON file syntax")
    sys_exit()

except PermissionError:
    print_error("Reading of the JSON file denied")
    sys_exit()

except IndexError:
    print_error("No JSON file provided")
    sys_exit()

except FileNotFoundError:
    print_error("File not found")
    sys_exit()


for json_object in json_file_contents:
    assem_url = ""

    if item_is_present("disabled", json_object):
        disabled = json_object["disabled"]

        if isinstance(disabled, bool):
            continue

    if item_is_present("domain_name", json_object):
        domain_name = json_object["domain_name"]

    else:
        print_error("Domain name is not defined")
        print_error(json_object)
        continue

    if item_is_present("scheme", json_object):
        scheme = json_object["scheme"]
        assem_url += scheme
        assem_url += "://"

    else:
        print_info("Correct URL scheme is not defined, using HTTP")
        assem_url += "http://"

    if item_is_present("username", json_object):
        user_name = json_object["username"]

        try:
            if len(user_name) <= 255:
                assem_url += user_name

            else:
                print_error("User name is to long (255 characters limit)")

        except TypeError:
            print_error("User name is not a string")
            print_error(json_object)
            continue

        if item_is_present("password", json_object):
            password = json_object["password"]

            try:
                if len(password) <= 255:
                    assem_url += ":"
                    assem_url += password

                else:
                    print_error("Password is to long (255 characters limit)")

            except TypeError:
                print_error("Password is not a string")
                print_error(json_object)
                continue

        assem_url += "@"

    try:
        assem_url += domain_name

    except TypeError:
        print_error("Domain name is not a string")
        print_error(json_object)
        continue

    if item_is_present("path", json_object):
        path = json_object["path"]

        try:
            if not path.startswith("/"):
                assem_url += "/"

            assem_url += path

        except (AttributeError, TypeError):
            print_error("Path is not a string")
            print_error(json_object)
            continue

        if item_is_present("fragment", json_object):
            fragment = json_object["fragment"]

            try:
                if not fragment.startswith("#"):
                    assem_url += "#"

                assem_url += fragment

            except (AttributeError, TypeError):
                print_error("Fragment is not a string")
                print_error(json_object)
                continue

        if item_is_present("query", json_object):
            query = json_object["query"]

            for index, key in enumerate(query):
                if key:

                    if not "?" in assem_url:
                        assem_url += "?"

                    assem_url += key

                    if query[key]:
                        assem_url += "="
                        assem_url += str(query[key])
                        assem_url += "&"

            if assem_url.endswith("&"):
                assem_url = re_sub("&$", "", assem_url)

    if item_is_present("port", json_object):
        port = json_object["port"]

        try:
            if 1 <= port <= 65535:
                assem_url += ":"
                assem_url += str(port)

            else:
                print_error("Port is not in range from 1 to 65535")

        except TypeError:
            print_error("Port is not an integer")

    pattern = re_compile(
        r'^https?://' # http:// or https://
        r'(?:[A-Z0-9]{1,255}:)?(?:[A-Z0-9]{1,255}@)?' # User name and optional password
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # Domain...
        r'localhost|' # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or IP
        r'(?::\d+)?' # Optional port
        r'(?:/?|[/?]\S+)$', re_ignore_case)

    if re_match(pattern, assem_url):
        print(assem_url)
        print()

    else:
        print_error("Not valid URL")
        print_error(json_object)
        # print_error(assem_url)
