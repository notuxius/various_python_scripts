#!/usr/bin/env python
import json
import sys
import os
import re


def print_error(error_text):
    sys.stderr.write("ERROR: " + error_text + "\n")


def print_info(info_text):
    print("INFO: " + info_text)


if len(sys.argv) != 2:
    print_error("To many or no arguments provided (one is required)")
    sys.exit()

# try:
with open(sys.argv[1]) as json_arg:
    json_file_contents = json.loads(json_arg.read())

# except:
#         print_error("Error in opening or processing the argument file")
#         sys.exit()

for json_object in json_file_contents:
    aggr_uri = ""

    if "disabled" in json_object:
        if isinstance(json_object["disabled"], bool):
            if json_object["disabled"]:
                continue

            else:
                print_info(
                    "All domains are enabled by default, no need to explicitly set disabled value as false for the domain:")

        elif str(json_object["disabled"]).strip() == "":
            print_info("Disabled value is empty for the domain:")

        else:
            print_error(
                "Disabled value not defined as bool true or false or for the object:")
            print_error(str(json_object))
            print()
            continue

    if "domain_name" not in json_object or not json_object["domain_name"]:
        print_error(
            "Required domain name is not defined or is empty for the object:")
        print_error(str(json_object))
        print()
        continue

    if ("scheme" in json_object and not json_object["scheme"]) or not "scheme" in json_object:
        print_info("Scheme is not defined for the domain, using http scheme:")
        aggr_uri += "http://"

    elif json_object["scheme"] == "http" or json_object["scheme"] == "https":
        aggr_uri += json_object["scheme"]
        aggr_uri += "://"

    else:
        print_error(
            "Valid (http or https) URI scheme is not defined for the domain:")

    if "username" in json_object and json_object["username"]:
        if isinstance(json_object["username"], str) and len(json_object["username"]) <= 255:
            aggr_uri += json_object["username"]

            if "password" in json_object and json_object["password"]:
                if isinstance(json_object["password"], str) and len(json_object["password"]) <= 255:
                    aggr_uri += ":"
                    aggr_uri += json_object["password"]

                else:
                    print_error(
                        "Password is not a string or is to long (255 characters limit) for the domain:")

            aggr_uri += "@"

        else:
            print_error(
                "User name is not a string or is to long (255 characters limit) for the domain:")

    aggr_uri += json_object["domain_name"]

    if "path" in json_object and json_object["path"]:
        if not isinstance(json_object["path"], str):
            print_error("Path is not a string for the domain:")
            json_object["path"] = str(json_object["path"])

        if not json_object["path"].startswith("/"):
            aggr_uri += "/"

        aggr_uri += json_object["path"]

        if "fragment" in json_object and json_object["fragment"]:
            if not isinstance(json_object["fragment"], str):
                print_error("Fragment is not a string for the domain:")
                json_object["fragment"] = str(json_object["fragment"])

            if not json_object["fragment"].startswith("#"):
                aggr_uri += "#"

            aggr_uri += json_object["fragment"]

        if "query" in json_object and json_object["query"]:
            if len(json_object["query"]) > 0:
                for index, key in enumerate(json_object["query"]):
                    if key:
                        if not "?" in aggr_uri:
                            aggr_uri += "?"

                        aggr_uri += key

                        if json_object["query"][key]:
                            aggr_uri += "="

                        if not isinstance(json_object["query"][key], str):
                            print_error(
                                "Value in query is not a string for the domain:")
                            json_object["query"][key] = str(
                                json_object["query"][key])

                        aggr_uri += json_object["query"][key]
                        aggr_uri += "&"

                    else:
                        print_error("Key in query is empty for the domain:")
                        continue

                if aggr_uri.endswith("&"):
                    aggr_uri = re.sub("&$", "", aggr_uri)

    else:
        print_error(
            "Not building possible remaining query because path is empty for the domain:")

    if "port" in json_object and json_object["port"]:
        try:    
            if 1 <= json_object["port"] <= 65535:
                aggr_uri += ":"
                aggr_uri += str(json_object["port"])

            else:
                print_error(
                    "Port is not in range from 1 to 65535 for the domain:")

        except TypeError:
            print_error(
                "Port is not an integer for the domain:")

    print(aggr_uri)
    print()
