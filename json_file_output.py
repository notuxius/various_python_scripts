#!/usr/bin/env python
from json import loads as json_loads
from json.decoder import JSONDecodeError
from sys import stderr as sys_stderr
from sys import exit as sys_exit
from sys import argv as sys_argv
from re import sub as re_sub


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


def scheme_is_correct(input_scheme):
    return bool(input_scheme in ("http", "https"))


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
    aggr_uri = ""

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

        if scheme_is_correct(scheme):
            aggr_uri += scheme
            aggr_uri += "://"

        else:
            print_error("URI scheme is not HTTP or HTTPS")
            print_error(json_object)
            continue

    # if not aggr_uri.startswith("http"):
    #     print_info("Correct URI scheme is not defined, using HTTP")
    #     aggr_uri += "http://"

    if item_is_present("username", json_object):
        user_name = json_object["username"]

        try:
            if len(user_name) <= 255:
                aggr_uri += user_name

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
                    aggr_uri += ":"
                    aggr_uri += password

                else:
                    print_error("Password is to long (255 characters limit)")

            except TypeError:
                print_error("Password is not a string")
                print_error(json_object)
                continue

        aggr_uri += "@"

    try:
        aggr_uri += domain_name

    except TypeError:
        print_error("Domain name is not a string")
        print_error(json_object)
        continue

    if item_is_present("path", json_object):
        path = json_object["path"]

        try:
            if not path.startswith("/"):
                aggr_uri += "/"

            aggr_uri += path

        except (AttributeError, TypeError):
            print_error("Path is not a string")
            print_error(json_object)
            continue

        if item_is_present("fragment", json_object):
            fragment = json_object["fragment"]

            try:
                if not fragment.startswith("#"):
                    aggr_uri += "#"

                aggr_uri += fragment

            except (AttributeError, TypeError):
                print_error("Fragment is not a string")
                print_error(json_object)
                continue

        if item_is_present("query", json_object):
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

    if item_is_present("port", json_object):
        port = json_object["port"]

        try:
            if 1 <= port <= 65535:
                aggr_uri += ":"
                aggr_uri += str(port)

            else:
                print_error("Port is not in range from 1 to 65535")

        except TypeError:
            print_error("Port is not an integer")

    print(aggr_uri)
    print()
