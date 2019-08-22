#!/usr/bin/env python
from sys import stderr as sys_stderr
from sys import exit as sys_exit
from sys import argv as sys_argv


def print_error(error):
    if isinstance(error, dict):
        sys_stderr.write(str(error) + "\n\n")

    sys_stderr.write("ERROR: " + str(error) + "\n")


def print_info(info):
    if isinstance(info, dict):
        print(str(info))

    print("INFO:", str(info))


try:
    with open(sys_argv[1]) as json_file:
        from json import loads as json_loads
        from json.decoder import JSONDecodeError

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

    try:
        disabled = json_object["disabled"]

        if isinstance(disabled, bool) and disabled:
            continue

    except KeyError:
        pass

    try:
        domain_name = json_object["domain_name"]

    except KeyError:
        continue

    if domain_name:
        try:
            scheme = json_object["scheme"]

            if scheme:
                if scheme in ("http", "https"):
                    assem_url += scheme
                    assem_url += "://"

                else:
                    print_error("URL scheme is wrong")
                    print_error(json_object)
                    continue

            else:
                print_info("URL scheme is empty, using HTTP")
                assem_url += "http://"

        except KeyError:
            print_info("URL scheme is not defined, using HTTP")
            assem_url += "http://"

        try:
            user_name = json_object["username"]

            try:
                if user_name:
                    if not len(user_name) <= 255:
                        print_info(
                            "User name is to long (255 characters limit)")
                        user_name = user_name[:255]

                    assem_url += user_name

                    try:
                        password = json_object["password"]

                        if password:
                            if not len(password) <= 255:
                                print_info(
                                    "Password is to long (255 characters limit)")
                                password = password[:255]

                            assem_url += ":"
                            assem_url += password

                    except TypeError:
                        print_error("Password is not a string")
                        print_error(json_object)
                        continue

                    except KeyError:
                        pass

                    assem_url += "@"

                else:
                    print_info("User name is empty")

            except TypeError:
                print_error("User name is not a string")
                print_error(json_object)
                continue

        except KeyError:
            pass

    else:
        print_error("Domain name is empty")
        print_error(json_object)
        continue

    try:
        assem_url += domain_name

    except TypeError:
        print_error("Domain name is not a string")
        print_error(json_object)
        continue

    try:
        path = json_object["path"]

        try:
            if not path.startswith("/"):
                assem_url += "/"

            assem_url += path

        except (AttributeError, TypeError):
            print_error("Path is not a string")
            print_error(json_object)
            continue

    except KeyError:
        pass

    try:
        fragment = json_object["fragment"]

        try:
            if not fragment.startswith("#"):
                assem_url += "#"

            assem_url += fragment

        except (AttributeError, TypeError):
            print_error("Fragment is not a string")
            print_error(json_object)
            continue

    except KeyError:
        pass

    try:
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
            from re import sub as re_sub

            assem_url = re_sub("&$", "", assem_url)

    except KeyError:
        pass

    try:
        port = json_object["port"]

        try:
            if 1 <= port <= 65535:
                assem_url += ":"
                assem_url += str(port)

            else:
                print_error("Port is not in range from 1 to 65535")

        except TypeError:
            print_error("Port is not an integer")

    except KeyError:
        pass

    from re import compile as re_compile
    from re import IGNORECASE as re_ignore_case
    from re import match as re_match

    pattern = re_compile(
        r'^https?://'  # http:// or https://
        # User name and optional password
        r'(?:[A-Z0-9]{1,255}:)?(?:[A-Z0-9]{1,255}@)?'
        # Domain name...
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or IP
        r'(?::\d+)?'  # Optional port
        r'(?:/?|[/?]\S+)$', re_ignore_case)  # Optional query and frament

    if re_match(pattern, assem_url):
        print(assem_url)
        print()

    else:
        print_error("Not valid URL")
        print(json_object)
        print()
