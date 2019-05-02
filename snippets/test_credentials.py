import os
from os.path import expanduser
import json

from harc.system.Profile import Profile


properties = dict()
properties['harc_dir'] = os.path.abspath('.')
properties['home.dir'] = expanduser('~')

credentials = Profile.credentials('poc_flask_docker', properties)
print(credentials)




