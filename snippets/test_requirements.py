from urllib.parse import urlparse, quote
from harc.system.Profile import Profile
from os.path import expanduser, exists

from harc.system.Requirements import Requirements
from harc.system.io.File import File

from harc.system.Git import Git

# print(exists("requirements.txt"))
#
# f = open("requirements.txt", 'rb')
# lines = f.readlines()
# f.close()
#
#
# # resolve the egg_name, so the egg_name is required for this work around.
# for line in lines:
#     line = line.decode('utf8').replace(chr(10), '')
#     if not line.startswith("#"):
#         index = line.find("#egg=")
#         if index != -1:
#             print(line)
#             egg_name = line[index+5::]
#
#             properties = dict()
#             properties['home.dir'] = expanduser('~')
#
#             credentials = Profile.credentials(egg_name, properties)
#             username = credentials['username']
#             password = credentials['password']
#
#             url = urlparse(line)
#             if url.scheme in ['git+http', 'git+https']:
#                 repository = url.scheme + "://'{0}':'{1}'@" + url.netloc + url.path
#                 repository = repository.format(quote(username), quote(password))
#                 print(repository)

properties = dict()
properties['home.dir'] = expanduser('~')

f = File('requirements.txt')
lines = f.read_lines()
credentials = Git.get_credentials()
print(credentials)
lines = Requirements.tokenize(lines, credentials)
#f.write_lines(lines)
print(lines)
