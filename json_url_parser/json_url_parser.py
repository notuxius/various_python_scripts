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
    def __init__(self, json_objects=None):
        from sys import argv as sys_argv

        self.url = ""
        self.output = {}

        from json import loads as json_loads
        from json.decoder import JSONDecodeError

        if json_objects:
            self.json_objects = json_loads(json_objects)

        else:
            self.json_objects = ""

            try:
                with open(sys_argv[1]) as json_file:
                    self.json_objects = json_loads(json_file.read())

            except IndexError:
                self.output[self.error()] = "No JSON file provided"

            except FileNotFoundError:
                self.output[self.error()] = "JSON file not found"

            except PermissionError:
                self.output[self.error()] = "Reading of the JSON file denied"

            except JSONDecodeError:
                self.output[self.error()] = "Bad JSON file syntax"

    # TODO fix workaround with self for importing into test_urls.py file
    def valid_url(self=""):
        return "Valid URL"

    def not_valid_url(self=""):
        return "Not valid URL"

    def error(self=""):
        return "Error:"

    def assem_urls(self):
        valid_url_num = 1
        not_valid_url_num = 1
        for json_object in self.json_objects:
            if self.is_disabled(json_object):
                continue

            self.url_add_scheme(json_object)
            self.url_add_user_password(json_object)
            self.url_add_domain_name(json_object)
            self.url_add_port(json_object)
            self.url_add_path(json_object)
            self.url_add_query(json_object)
            self.url_add_fragment(json_object)

            if self.is_correct_url():
                self.output[f"{self.valid_url()} #{valid_url_num}:"] = self.url
                valid_url_num += 1

            else:
                self.output[f"{self.not_valid_url()} #{not_valid_url_num}:"] = json_object
                not_valid_url_num += 1

            self.url = ""

        return self.output

    def print_output(self):
        from sys import stderr as sys_stderr

        self.assem_urls()

        for header in sorted(self.output):
            if self.error() in header or self.not_valid_url() in header:
                sys_stderr.write(str(header))
                sys_stderr.write("\n")
                sys_stderr.write(str(self.output[header]))
                sys_stderr.write("\n")
                sys_stderr.write("\n")

            else:
                print(header)
                print(self.output[header])
                print()

    def is_disabled(self, json_object):
        try:
            disabled = json_object["disabled"]

            if isinstance(disabled, bool) and disabled:
                return True

        except KeyError:
            return False

    def url_add_scheme(self, json_object):
        try:
            scheme = json_object["scheme"]

            if scheme:
                self.url += scheme
                self.url += "://"

            else:
                self.url += "http://"

        except KeyError:
            self.url += "http://"

    def url_add_user_password(self, json_object):
        try:
            user_name = json_object["user_name"]

            # try:
            if user_name:
                self.url += user_name

                try:
                    password = json_object["password"]

                    if password:
                        self.url += ":"
                        self.url += password

                # except TypeError:
                #     self.output.append("ePassword is not a string")

                except KeyError:
                    pass

                self.url += "@"

            # except TypeError:
            #     self.output.append("eUser name is not a string")

        except KeyError:
            return False

        # else:
        #     raise ParseError("eURL scheme is wrong")

    def url_add_domain_name(self, json_object):
        try:
            domain_name = json_object["domain_name"]

        except KeyError:
            return False

        if domain_name:
            try:
                self.url += domain_name

            except TypeError:
                # self.output.append("eDomain name is not a string")
                pass

        # else:
        #     self.output.append("eDomain name is empty")

    def url_add_path(self, json_object):
        try:
            path = json_object["path"]

            # try:
            if not path.startswith("/"):
                self.url += "/"

            self.url += path

            # except (AttributeError, TypeError):
            #     self.output.append("ePath is not a string")

        except KeyError:
            return False

    def url_add_fragment(self, json_object):
        try:
            fragment = json_object["fragment"]

            # try:
            if not fragment.startswith("#"):
                self.url += "#"

            self.url += fragment

            # except (AttributeError, TypeError):
            #     self.output.append("eFragment is not a string")

        except KeyError:
            pass

    def url_add_query(self, json_object):
        try:
            query = json_object["query"]

            for _, key in enumerate(query):
                if not "?" in self.url:
                    self.url += "?"

                self.url += key
                self.url += "="
                self.url += str(query[key])
                self.url += "&"

            if self.url.endswith("&"):
                from re import sub as re_sub

                self.url = re_sub("&$", "", self.url)

        except KeyError:
            pass

    def url_add_port(self, json_object):
        try:
            port = json_object["port"]

            try:
                if 1 <= port <= 65535:
                    self.url += ":"
                    self.url += str(port)

                # else:
                #     self.output.append("ePort is not in range from 1 to 65535")

            except TypeError:
                # self.output.append("ePort is not an integer")
                pass

        except KeyError:
            pass

    def is_correct_url(self):
        from re import compile as re_compile
        from re import IGNORECASE as re_ignore_case
        from re import match as re_match

        # TODO improve regex - hangs on some combination of input
        pattern = re_compile(
            r"^https?:\/{2}(?:(?:[^:\s]{1,255}:)?[^:\s]{1,255}@)?"
            r"(?:(?:[a-z-]{1,63}\.)+(?:[a-z]{1,63})|"
            r"(?:(?:[0-9]{1,3}\.){3}[0-9]{1,3}))"
            r"(?::[0-9]{1,5})?(?:(?:\/[^\/])?(?:[a-z0-9]{1,2000})?){1,255}"
            r"(?:(?:\?[a-z0-9_.~-]{1,255}=[a-z0-9_.~-]{1,255})"
            r"(?:&[a-z0-9_.~-]{1,255}=[a-z0-9_.~-]{1,255}){0,255})?"
            r"(?:#[a-z0-9]{0,255})?\/?$", re_ignore_case)

        if re_match(pattern, self.url):
            return True

        return False


json_urls = JsonUrlParser()
# json_urls = JsonUrlParser("""[{
#     "scheme": "https",
#     "domain_name": "www.duckduckgo.com",
#     "path": "name/of/path",
#     "port": 7778,
#     "user_name": "user",
#     "password": "pass",
#     "fragment": "asdf",
#     "query": {
#         "qk1": "queryvalue1",
#         "querykey2": "queryvalue2"
#         }
# }]""")
# json_urls.assem_urls()
# print(json_urls.assem_urls().items()
json_urls.print_output()
