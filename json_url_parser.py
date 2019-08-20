#!/usr/bin/env python


# class ParseError(Exception):
#     def __init__(self, error):
#         super(ParseError, self).__init__(error)
#         self.error = error

#     def __str__(self):
#         if isinstance(self.error, dict):
#             return (str(self.error) + "\n\n")

#         return ("ERROR: " + str(self.error) + "\n")


# class Info(ParseError):
#     def __str__(self):
#         if isinstance(self.error, dict):
#             return (str(self.error) + "\n\n")

#         return ("INFO: " + str(self.error) + "\n")


class JsonUrlParser():
    def __init__(self):
        from sys import argv as sys_argv
        from sys import stderr as sys_stderr
        # from sys import exit as sys_exit

        self.json_file_cont = ""
        self.url = ""

        try:
            with open(sys_argv[1]) as self.json_file:
                from json import loads as json_loads
                from json.decoder import JSONDecodeError

                self.json_file_cont = json_loads(self.json_file.read())

        except IndexError:
            # raise Info("No JSON file provided")
            sys_stderr.write("No JSON file provided")
            # sys_exit()

        except FileNotFoundError:
            sys_stderr.write("JSON file not found")
            # sys_exit()

        except PermissionError:
            sys_stderr.write("Reading of the JSON file denied")
            # sys_exit()

        except JSONDecodeError:
            sys_stderr.write("Bad JSON file syntax")
            # sys_exit()

    def parse_urls(self):
        for json_object in self.json_file_cont:
            if self.is_disabled(json_object):
                continue

            self.add_scheme(json_object)
            self.add_user_password(json_object)
            self.add_domain_name(json_object)
            self.add_path(json_object)
            self.add_fragment(json_object)
            self.add_query(json_object)
            self.add_port(json_object)

            if self.is_url(json_object):
                self.print_reset_url()

    def is_disabled(self, json_object):
        try:
            disabled = json_object["disabled"]

            if isinstance(disabled, bool) and disabled:
                return True

        except KeyError:
            return False

    def add_scheme(self, json_object):
        try:
            scheme = json_object["scheme"]

            if scheme:
                if scheme in ("http", "https"):
                    self.url += scheme
                    self.url += "://"

                else:
                    print("eURL scheme is wrong")
                    print(json_object)

            else:
                print("iURL scheme is empty, using HTTP")
                self.url += "http://"

        except KeyError:
            print("iURL scheme is not defined, using HTTP")
            self.url += "http://"

    def add_user_password(self, json_object):
        try:
            user_name = json_object["username"]

            try:
                if user_name:
                    if not len(user_name) <= 255:
                        print(
                            "iUser name is to long (255 characters limit)")
                        user_name = user_name[:255]

                    self.url += user_name

                    try:
                        password = json_object["password"]

                        if password:
                            if not len(password) <= 255:
                                print(
                                    "iPassword is to long (255 characters limit)")
                                password = password[:255]

                            self.url += ":"
                            self.url += password

                    except TypeError:
                        print("ePassword is not a string")
                        print(json_object)
                        return False

                    except KeyError:
                        pass

                    self.url += "@"

                else:
                    print("iUser name is empty")

            except TypeError:
                print("eUser name is not a string")
                print(json_object)
                return False

        except KeyError:
            return False

        # else:
        #     raise ParseError("URL scheme is wrong")
        # print_error(json_object)
        # continue

    def add_domain_name(self, json_object):
        try:
            domain_name = json_object["domain_name"]

        except KeyError:
            return False

        if domain_name:
            try:
                self.url += domain_name

            except TypeError:
                print("eDomain name is not a string")
                print(json_object)
                return False

        else:
            print("eDomain name is empty")
            print(json_object)
            return False

    def add_path(self, json_object):
        try:
            path = json_object["path"]

            try:
                if not path.startswith("/"):
                    self.url += "/"

                self.url += path

            except (AttributeError, TypeError):
                print("ePath is not a string")
                print(json_object)
                return False

        except KeyError:
            return False

    def add_fragment(self, json_object):
        try:
            fragment = json_object["fragment"]

            try:
                if not fragment.startswith("#"):
                    self.url += "#"

                self.url += fragment

            except (AttributeError, TypeError):
                print("eFragment is not a string")
                print(json_object)
                return False

        except KeyError:
            return False

    def add_query(self, json_object):
        try:
            query = json_object["query"]

            for _, key in enumerate(query):
                if key:
                    if not "?" in self.url:
                        self.url += "?"

                    self.url += key

                    if query[key]:
                        self.url += "="
                        self.url += str(query[key])
                        self.url += "&"

            if self.url.endswith("&"):
                from re import sub as re_sub

                self.url = re_sub("&$", "", self.url)

        except KeyError:
            pass

    def add_port(self, json_object):
        try:
            port = json_object["port"]

            try:
                if 1 <= port <= 65535:
                    self.url += ":"
                    self.url += str(port)

                else:
                    print("ePort is not in range from 1 to 65535")

            except TypeError:
                print("ePort is not an integer")

        except KeyError:
            pass

    def is_url(self, json_object):
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

        if re_match(pattern, self.url):
            return True

        print("eNot valid URL")
        print(json_object)
        return False

    def print_reset_url(self):
        print(self.url)
        print()

        self.url = ""


json_url = JsonUrlParser()
json_url.parse_urls()
