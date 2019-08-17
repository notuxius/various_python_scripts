#!/usr/bin/env python
from json import loads as json_loads
from json.decoder import JSONDecodeError
from sys import stderr as sys_stderr
from sys import exit as sys_exit
from sys import argv as sys_argv
from re import sub as re_sub


def print_error(error):
    if isinstance(error, dict):
        sys_stderr.write(str(error) + "\n")

    else:
        sys_stderr.write("ERROR: " + str(error) + "\n")


def print_info(info):
    if isinstance(info, dict):
        print(str(info))

    else:
        print("INFO: " + str(info))

# TODO Split this func into two
def item_is_present_and_has_correct_type(item, item_type, input_json_object):
    return bool(item in input_json_object and
                isinstance(input_json_object[item], item_type) and input_json_object[item])


def scheme_is_correct(input_scheme):
    return bool(input_scheme in ("http", "https"))


try:
    with open(sys_argv[1]) as json_arg:
        json_file_contents = json_loads(json_arg.read())

except JSONDecodeError:
    print_error("Bad JSON file syntax")
    sys_exit()

except PermissionError:
    print_error("Reading of the JSON file denied")

except IndexError:
    print_error("No JSON file provided")
    sys_exit()

except FileNotFoundError:
    print_error("File not found")
    sys_exit()


for json_object in json_file_contents:
    aggr_uri = ""

    if item_is_present_and_has_correct_type("disabled", bool, json_object):
        continue

    if not item_is_present_and_has_correct_type("domain_name", str, json_object):
        print_error("Required domain name is not defined or is empty:")
        print_error(json_object)
        print()
        continue

    if item_is_present_and_has_correct_type("scheme", str, json_object):
        scheme = json_object["scheme"]

        if scheme_is_correct(scheme):
            aggr_uri += scheme
            aggr_uri += "://"

    if not aggr_uri.startswith("http"):
        print_info("Correct URI scheme is not defined, using HTTP:")
        aggr_uri += "http://"

    if item_is_present_and_has_correct_type("username", str, json_object):
        user_name = json_object["username"]

        if len(user_name) <= 255:
            aggr_uri += user_name

            if item_is_present_and_has_correct_type("password", str, json_object):
                password = json_object["password"]

                if len(password) <= 255:
                    aggr_uri += ":"
                    aggr_uri += password

                else:
                    print_error("Password is to long (255 characters limit):")

            aggr_uri += "@"

        else:
            print_error("User name is to long (255 characters limit):")

    aggr_uri += json_object["domain_name"]

    if item_is_present_and_has_correct_type("path", str, json_object):
        path = json_object["path"]

        if not path.startswith("/"):
            aggr_uri += "/"

        aggr_uri += path

        if item_is_present_and_has_correct_type("fragment", str, json_object):
            fragment = json_object["fragment"]

            if not fragment.startswith("#"):
                aggr_uri += "#"

            aggr_uri += fragment

        if item_is_present_and_has_correct_type("query", dict, json_object):
            query = json_object["query"]

            for index, key in enumerate(query):

                if key:

                    if not "?" in aggr_uri:
                        aggr_uri += "?"

                    aggr_uri += key

                    if query[key]:
                        aggr_uri += "="
                        aggr_uri += str(query[key])
                        aggr_uri += "&"

            if aggr_uri.endswith("&"):
                aggr_uri = re_sub("&$", "", aggr_uri)

    if item_is_present_and_has_correct_type("port", int, json_object):
        port = json_object["port"]

        if 1 <= port <= 65535:
            aggr_uri += ":"
            aggr_uri += port

        else:
            print_error("Port is not in range from 1 to 65535:")

    print(aggr_uri)
    print()
