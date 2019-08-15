#!/usr/bin/env python
import json
import sys

if len(sys.argv) < 2:
    sys.exit("ERROR: No arguments provided (one is required)")
elif len(sys.argv) > 2:
    sys.exit("ERROR: To many arguments provided (one is required)")

# try:
with open(sys.argv[1]) as json_arg:
    json_file_contents = json.loads(json_arg.read())

# except:
#         sys.exit("Error in opening or processing the argument file")

for json_object in json_file_contents:
    aggr_uri = ""

    if "disabled" in json_object:
        if isinstance(json_object["disabled"], bool):
            if json_object["disabled"]:
                continue

            else:
                print("INFO: All domains are enabled by default, no need to explicitly set disabled value as false for the domain:")

        elif str(json_object["disabled"]).strip() == "":
                print("INFO: Disabled value is empty for the domain:")

        else:
            sys.stderr.write("ERROR: Disabled value not defined as bool true or false or for the domain:\n" + 
            str(json_object) + "\n\n")
            continue

    if "domain_name" not in json_object or not json_object["domain_name"]:
        sys.stderr.write("ERROR: Required domain name not found for the domain:\n" +
                         str(json_object) + "\n")
        continue

    if ("scheme" in json_object and not json_object["scheme"]) or not "scheme" in json_object:
        print("INFO: Scheme is not defined for the domain, using http scheme:")
        aggr_uri += "http://"

    elif json_object["scheme"] == "http" or json_object["scheme"] == "https":
            aggr_uri += json_object["scheme"]
            aggr_uri += "://"
        
    else:
        sys.stderr.write("ERROR: Valid (http or https) URI scheme is not defined for the domain:\n")

    if "username" in json_object and json_object["username"]:
        if isinstance(json_object["username"], str) and len(json_object["username"]) <= 255:
            if "password" in json_object and json_object["password"]:
                if isinstance(json_object["password"], str) and len(json_object["password"]) <= 255:
                    aggr_uri += json_object["username"]
                    aggr_uri += ":"
                    aggr_uri += json_object["password"]
                    aggr_uri += "@"
    
                else:
                    sys.stderr.write("ERROR: Password is not a string or is to long (255 characters limit) for the domain:\n")
        
        else:
            sys.stderr.write("ERROR: User name is not a string or is to long (255 characters limit) for the domain:\n")

        if not "password" in json_object or not json_object["password"]:
            print("INFO: Password is empty for the domain:")
            aggr_uri += json_object["username"]
            aggr_uri += "@"

    elif "password" in json_object and json_object["password"]:
        sys.stderr.write("ERROR: Password is not a string or to long (255 characters limit) and/or password without user name for the domain:\n")

    if ("username" in json_object and not json_object["username"]) and ("password" in json_object and not json_object["password"]):
        print("INFO: User name and password are empty for the domain:")

    aggr_uri += json_object["domain_name"]

    if "path" in json_object:

        if str(json_object["path"]):

            if not str(json_object["path"]).startswith("/"):
                aggr_uri += "/"

            if isinstance(json_object["path"], str):
                aggr_uri += json_object["path"]

            else:
                print("INFO: Path is not a string for the domain:")
                aggr_uri += str(json_object["path"])

            if "fragment" in json_object and json_object["fragment"]:
                aggr_uri += "#"

                if isinstance(json_object["fragment"], str):
                    aggr_uri += json_object["fragment"]

                else:
                    print("INFO: Fragment is not a string for the domain:")
                    aggr_uri += str(json_object["fragment"])

            else:
                print("INFO: Fragment is empty for the domain:")

            if "query" in json_object:
                if len(json_object["query"]) != 0:
                    aggr_uri += "?"

                    for index, key in enumerate(json_object["query"]):
                        if not key:
                            sys.stderr.write(
                                "ERROR: Missing key in the domain query:")

                        if not json_object["query"][key]:
                            sys.stderr.write(
                                "ERROR: Missing value in the domain query:")

                        aggr_uri += key
                        aggr_uri += "="
                        aggr_uri += str(json_object["query"][key])

                        if index != len(json_object["query"]) - 1:
                            aggr_uri += "&"

                else:
                    sys.stderr.write("ERROR: Empty query for the domain:\n")

        else:
            sys.stderr.write("ERROR: Not building possible remaining query because path is empty for the domain:\n")
        
    if "port" in json_object and json_object["port"]:
        if str(json_object["port"]).startswith(":"):
            json_object["port"] = json_object["port"].replace(":", "")

        try:
            if 1 <= int(json_object["port"]) <= 65535:
                aggr_uri += ":"
                aggr_uri += str(json_object["port"])
            
            else:
                sys.stderr.write("ERROR: Port is not in range from 1 to 65535 for the domain:\n")

        except ValueError:
            sys.stderr.write("ERROR: Port is not an integer in range from 1 to 65535 for the domain:\n")

    print(aggr_uri)
    print()
