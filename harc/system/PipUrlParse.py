from urllib.parse import urlparse, quote


class PipUrlParse:
    def __init__(self, url):
        self.__url = url
        self.__parsed_url = urlparse(url)

    def get_url(self):
        return self.__url

    def get_parsed_url(self):
        return self.__parsed_url

    def egg_name(self):
        url = self.get_url()
        index = url.find("#egg=")
        if index != -1:
            egg_name = url[index + 5::]
            return egg_name

    def get_hostname(self):
        parsed_url = self.get_parsed_url()
        if parsed_url.hostname:
            return parsed_url.hostname
        return None

    def tokenize(self, username, password):
        """
        Update the url with username and password in the netloc part

        :param username:
        :param password:

        :return: A new url
        """
        parsed_url = self.get_parsed_url()

        if parsed_url.scheme in ['git+http', 'git+https']:
            # only tokenize if the netloc is the same as hostname
            # (i.e. does not already contain credentials)
            if parsed_url.netloc == parsed_url.hostname:
                repository = "{}://{}:{}@{}{}{}".format(
                    parsed_url.scheme,
                    username, password,
                    parsed_url.hostname,
                    parsed_url.path,
                    ';{}'.format(parsed_url.params) if parsed_url.params else '',
                    '?{}'.format(parsed_url.query) if parsed_url.query else '',
                    '#{}'.format(parsed_url.fragment) if parsed_url.fragment else '',
                )
                return repository

        # If the above conditions do not apply, just return the url
        return self.get_url()
