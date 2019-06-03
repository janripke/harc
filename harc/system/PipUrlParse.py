from urllib.parse import urlparse, quote


class PipUrlParse:
    def __init__(self, url):
        self.__url = url

    def get_url(self):
        return self.__url

    def egg_name(self):
        url = self.get_url()
        index = url.find("#egg=")
        if index != -1:
            egg_name = url[index + 5::]
            return egg_name

    def tokenize(self, username, password):
        url = self.get_url()
        repository = url
        url = urlparse(url)
        if url.scheme in ['git+http', 'git+https']:
            egg_name = self.egg_name()

            # only tokenize if the netloc resolves to a single hostname.
            if len(url.netloc.split('@')) == 1:
                repository = url.scheme + "://{0}:{1}@" + url.netloc + url.path + "#egg=" + egg_name
                repository = repository.format(quote(username), quote(password))
        return repository
