from harc.system.Git import *
from urllib.parse import urlparse, quote
from harc.system.System import System
import uuid
import os


folder = '/home/user/workspace/harc/snippets/test'
repository_url = 'https://gitlab.et-scm.com/MDP/mdp-api.git'

# set identifier, reflecting the checkout folder to build this release.
name = uuid.uuid4().hex
# required files are copied into build_folder that is zipped and uploaded to s3




url = urlparse(repository_url)
repository = repository_url

username = 'orucs'
password = 'Oxyma1234'

project_name ="mdp_api"

if url.scheme in ['http', 'https']:
    if not username:
        raise PluginException("no username")

    if not password:
        raise PluginException("no password")

    repository = url.scheme + "://'{0}':'{1}'@" + url.netloc + url.path
    repository = repository.format(quote(username), quote(password))



Git.clone(repository, os.path.join(folder, name))

branch = 'stable'
r = Git.checkout_branch(branch, os.path.join(folder, name))

print(r)
