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
        from sys import stderr as sys_stderr
        # from sys import exit as sys_exit

        # if self.url and self.is_url(self.url):
        #     print("123")

        self.url = ""
        self.ready_urls = []

        from json import loads as json_loads
        from json.decoder import JSONDecodeError

        if json_objects:
            self.json_objects = json_loads(json_objects)

            try:
                if sys_argv[1]:
                    print("Skipping reading of JSON file")

            except IndexError:
                pass

        else:
            self.json_objects = ""

            try:
                with open(sys_argv[1]) as json_file:
                    self.json_objects = json_loads(json_file.read())

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

    def assem_urls(self):
        for json_object in self.json_objects:
            if self.is_disabled(json_object):
                continue

            # Use format?
            self.add_scheme(json_object)
            self.add_user_password(json_object)
            self.add_domain_name(json_object)
            self.add_port(json_object)
            self.add_path(json_object)
            self.add_query(json_object)
            self.add_fragment(json_object)

            if self.is_url(json_object):
                self.ready_urls.append(self.url)

            else:
                self.ready_urls.append("Not valid URL")

            self.url = ""

        return self.ready_urls

    def print_urls(self):
        self.assem_urls()

        for url in self.ready_urls:
            print(url)
            print()

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
            user_name = json_object["user_name"]

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
            r"^https?:\/{2}(?:[^:\s]{1,255}:[^:\s]{1,255}@|[^:\s]{1,255}@)?"
            r"((?:[a-z-]{1,255}\.)+(?:[a-z]{1,6})|"
            r"(?:[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))"
            r"(?::[0-9]{1,5})?((?:\/[^\/])?(?:[a-z0-9]{1,255})?){1,255}"
            r"(?:(?:\?[a-z0-9_.~-]{1,255}=[a-z0-9_.~-]{1,255}&"
            r"[a-z0-9_.~-]{1,255}=[a-z0-9_.~-]{1,255}){1,255}|"
            r"\?[a-z0-9_.~-]{1,255}=(?:[a-z0-9_.~-]{1,255}))?#?"
            r"(?:[a-z0-9]{1,255})?\/?$", re_ignore_case)

        if re_match(pattern, self.url):
            # print(self.url)
            return True

        print("eNot valid URL")
        print(json_object)
        print()
        return False

    # def print_urls(self):
    #     print(self.assem_urls())


# json_urls = JsonUrlParser()
json_urls = JsonUrlParser("""[{
    "scheme": "https",
    "domain_name": "www.google.com",
    "path": "name/of/path",
    "port": 777,
    "user_name": "user",
    "password": "pass",
    "fragment": "",
    "query": {
        "": "queryvalue1",
        "querykey2": "queryvalue2"
        }
}]""")
# json_urls.assem_urls()
print(json_urls.assem_urls())
# json_urls.print_urls()
