from urllib.parse import urlparse

# "https://'{0}':'{1}'@github.com/janripke/harc.git"
repo = "https://github.com/janripke/harc.git"

url = urlparse(repo)
url = url.scheme + "//'{0}':'{1}'@" + url.netloc + url.path

print(url)
